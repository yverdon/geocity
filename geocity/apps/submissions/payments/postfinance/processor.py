from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.urls import reverse
from django.utils import timezone
from postfinancecheckout import (
    Configuration,
    Environment,
    LineItemAttribute,
    TransactionEnvironmentSelectionStrategy,
    TransactionState,
)
from postfinancecheckout.api import (
    TransactionPaymentPageServiceApi,
    TransactionServiceApi,
)
from postfinancecheckout.models import LineItem, LineItemType, TransactionCreate

from ..processors import PaymentProcessor
from .models import PostFinanceTransaction


class PostFinanceCheckoutProcessor(PaymentProcessor):
    name = "PostFinance Checkout"
    identifier = "PostFinance"
    transaction_class = PostFinanceTransaction
    required_settings = [
        "PAYMENT_PROCESSING_TEST_ENVIRONMENT",
    ]
    required_params = ["space_id", "user_id", "api_key"]

    def __init__(self, space_id, user_id, api_key):
        super().__init__()
        self.config = Configuration(
            user_id=user_id,
            api_secret=api_key,
        )
        self.space_id = space_id
        self.transaction_service_api = None
        self.transaction_payment_page_service = None

    def _get_transaction_service_api(self):
        if getattr(self, "transaction_service_api", None) is None:
            self.transaction_service_api = TransactionServiceApi(
                configuration=self.config
            )
        return self.transaction_service_api

    def _get_transaction_payment_page_service_api(self):
        if getattr(self, "transaction_payment_page_service", None) is None:
            self.transaction_payment_page_service = TransactionPaymentPageServiceApi(
                configuration=self.config
            )
        return self.transaction_payment_page_service

    def create_merchant_transaction(self, request, submission, transaction):
        """
        Creates a transaction on PostFinance Checkout. The transaction contains 1 line item with:
        - Name: The submission's price's text (description of the price)
        - Unique ID: The submission's ID
        - SKU: The submission's original price instance's ID
        - Attribute "Compte interne": the internal_accoutn value specified in PaymentSettings

        Returns a dict with the following entries:
        {
            "merchant_reference": <str, PostFinance's transaction identifier>,
            "authorization_timeout_on": <datetime, when the transaction times out, if not paid/cancelld>,
            "payment_page_url": <str, the URL when payment is done on PostFinance>,
        }
        """
        transaction_service = self._get_transaction_service_api()
        transaction_payment_page_service = (
            self._get_transaction_payment_page_service_api()
        )

        # If the form is None interrupt payment flow
        if not submission.get_form_for_payment() or not submission.requires_payment():
            raise SuspiciousOperation

        internal_account = (
            submission.get_form_for_payment().payment_settings.internal_account
        )

        attribute = LineItemAttribute(label="Compte interne", value=internal_account)

        line_item = LineItem(
            name=submission.price.text,
            unique_id=str(submission.pk),
            sku=str(submission.price.original_price.pk),
            quantity=1,
            attributes={"internal_account": attribute},
            amount_including_tax=float(submission.price.amount),
            type=LineItemType.PRODUCT,
        )
        environment_selection_strategy = (
            TransactionEnvironmentSelectionStrategy.FORCE_TEST_ENVIRONMENT
            if settings.PAYMENT_PROCESSING_TEST_ENVIRONMENT
            else TransactionEnvironmentSelectionStrategy.USE_CONFIGURATION
        )
        environment = (
            Environment.PREVIEW
            if settings.PAYMENT_PROCESSING_TEST_ENVIRONMENT
            else Environment.LIVE
        )
        success_url = request.build_absolute_uri(
            reverse("submissions:confirm_transaction", kwargs={"pk": transaction.pk})
        )
        failed_url = request.build_absolute_uri(
            reverse("submissions:fail_transaction", kwargs={"pk": transaction.pk})
        )

        merchant_transaction = TransactionCreate(
            line_items=[line_item],
            auto_confirmation_enabled=True,
            currency=submission.price.currency,
            environment=environment,
            environment_selection_strategy=environment_selection_strategy,
            success_url=success_url,
            failed_url=failed_url,
        )
        transaction_create = transaction_service.create(
            space_id=self.space_id, transaction=merchant_transaction
        )

        payment_page_url = transaction_payment_page_service.payment_page_url(
            space_id=self.space_id, id=transaction_create.id
        )

        return {
            "merchant_reference": transaction_create.merchant_reference,
            "authorization_timeout_on": transaction_create.authorization_timeout_on,
            "payment_page_url": payment_page_url,
        }

    def _get_transaction_status(self, transaction):
        transaction_service = self._get_transaction_service_api()
        merchant_transaction = transaction_service.read(
            self.space_id, transaction.merchant_reference
        )
        return merchant_transaction.state

    def is_transaction_authorized(self, transaction):
        # The following are considered to be the "success" statuses by PostFinance
        status = self._get_transaction_status(transaction)
        return status in (
            TransactionState.FULFILL,
            TransactionState.COMPLETED,
            TransactionState.AUTHORIZED,
        )

    def _create_internal_transaction(self, submission):
        # If there is a related existing transaction, which:
        # 1. Is still within the PostFinance authorization time window
        # 2. Has the same amount and currency
        #    (if it is different, it means that the user has chosen a different price)
        # 3. Is unpaid
        # Then we can reuse it, instead of re-generating another one
        existing_transaction = self.transaction_class.objects.filter(
            submission_price=submission.submission_price,
            amount=submission.submission_price.amount,
            currency=submission.submission_price.currency,
            status=self.transaction_class.STATUS_UNPAID,
            authorization_timeout_on__gt=timezone.now(),
        ).first()
        if existing_transaction:
            return existing_transaction, False
        return super(PostFinanceCheckoutProcessor, self)._create_internal_transaction(
            submission
        )

    def _save_merchant_data(self, transaction, merchant_transaction_data):
        transaction.authorization_timeout_on = merchant_transaction_data[
            "authorization_timeout_on"
        ]
        transaction.payment_url = merchant_transaction_data["payment_page_url"]
        return super(PostFinanceCheckoutProcessor, self)._save_merchant_data(
            transaction, merchant_transaction_data
        )
