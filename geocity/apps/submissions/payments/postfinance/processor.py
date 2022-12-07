from django.conf import settings
from django.urls import reverse
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
        transaction_service = self._get_transaction_service_api()
        transaction_payment_page_service = (
            self._get_transaction_payment_page_service_api()
        )

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
            "payment_page_url": payment_page_url,
        }

    def _get_transaction_status(self, transaction):
        transaction_service = self._get_transaction_service_api()
        merchant_transaction = transaction_service.read(
            self.space_id, transaction.merchant_reference
        )
        return merchant_transaction.state

    def is_transaction_fulfilled(self, transaction):
        status = self._get_transaction_status(transaction)
        return status == TransactionState.FULFILL
