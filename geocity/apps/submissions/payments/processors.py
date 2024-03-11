from django.conf import settings
from django.urls import reverse


class MissingPaymentProcessorSettingError(Exception):
    pass


class PaymentProcessor:
    required_settings = None
    name = None
    identifier = None
    transaction_class = None

    def _check_required_settings(self):
        if self.required_settings is not None:
            for setting in self.required_settings:
                try:
                    getattr(settings, setting)
                except AttributeError:
                    raise MissingPaymentProcessorSettingError(
                        f"Missing setting {setting} to configure payment processor {self.name} !"
                    )

    def __init__(self):
        self._check_required_settings()

    def create_merchant_transaction(
        self, request, submission, transaction, extra_kwargs=None
    ):
        """
        Returns a dict with the merchant transaction data. Example:
        {
            'transaction_id': <payment processors' transaction id>,
            'payment_page_url': <payment_page_url>
        }
        """
        raise NotImplementedError

    def _create_internal_transaction(
        self, submission, transaction_type=None, override_price=None
    ):
        price = submission.get_submission_price()
        if override_price is None:
            currency = price.currency
            amount = price.amount
        else:
            currency = override_price.currency
            amount = override_price.amount
        create_kwargs = {
            "submission_price": price,
            "transaction_id": 0,
            "amount": amount,
            "currency": currency,
        }
        if transaction_type is not None:
            create_kwargs["transaction_type"] = transaction_type
        return (
            self.transaction_class.objects.create(**create_kwargs),
            True,
        )

    def _save_merchant_data(self, transaction, merchant_transaction_data):
        transaction.transaction_id = merchant_transaction_data["transaction_id"]
        transaction.save()

    def create_free_transaction(self, submission):
        empty_transaction, __ = self._create_internal_transaction(submission)
        empty_transaction.transaction_id = str(submission.pk)
        empty_transaction.set_paid()
        empty_transaction.save()
        return empty_transaction

    def create_transaction_and_return_payment_page_url(self, submission, request):
        transaction, is_new_transaction = self._create_internal_transaction(submission)
        if is_new_transaction:
            merchant_transaction_data = self.create_merchant_transaction(
                request, submission, transaction
            )
            self._save_merchant_data(transaction, merchant_transaction_data)
            return merchant_transaction_data["payment_page_url"]
        else:
            return transaction.payment_url

    def create_prolongation_transaction_and_return_payment_page_url(
        self, submission, prolongation_price, prolongation_date, request
    ):
        transaction, is_new_transaction = self._create_internal_transaction(
            submission,
            transaction_type=self.transaction_class.TYPE_PROLONGATION,
            override_price=prolongation_price,
        )
        if is_new_transaction:
            merchant_transaction_data = self.create_merchant_transaction(
                request,
                submission,
                transaction,
                extra_kwargs={
                    "amount": prolongation_price.amount,
                    "currency": prolongation_price.currency,
                    "text": prolongation_price.text,
                    "pk": prolongation_price.pk,
                    "success_url": request.build_absolute_uri(
                        reverse(
                            "submissions:confirm_prolongation_transaction",
                            kwargs={
                                "pk": transaction.pk,
                                "prolongation_date": prolongation_date,
                            },
                        )
                    ),
                    "failed_url": request.build_absolute_uri(
                        reverse(
                            "submissions:fail_prolongation_transaction",
                            kwargs={"pk": transaction.pk},
                        )
                    ),
                },
            )
            self._save_merchant_data(transaction, merchant_transaction_data)
            return merchant_transaction_data["payment_page_url"]
        else:
            return transaction.payment_url

    def _get_transaction_status(self, transaction):
        raise NotImplementedError

    def is_transaction_authorized(self, transaction):
        raise NotImplementedError
