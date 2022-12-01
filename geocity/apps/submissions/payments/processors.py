from django.conf import settings


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

    def create_merchant_transaction(self, submission, request):
        """
        Returns a dict with the merchant transaction data. Example:
        {
            'merchant_reference': <payment processors' transaction id>,
            'payment_page_url': <payment_page_url>
        }
        """
        raise NotImplementedError

    def _create_internal_transaction(self, submission, merchant_transaction_data):
        price = submission.get_submission_price()
        self.transaction_class.objects.create(
            submission_price=price,
            merchant_reference=merchant_transaction_data["merchant_reference"],
            amount=price.amount,
            currency=price.currency,
        )

    def create_transaction_and_return_payment_page_url(self, submission, request):
        merchant_transaction_data = self.create_merchant_transaction(
            submission, request
        )
        self._create_internal_transaction(submission, merchant_transaction_data)
        return merchant_transaction_data["payment_page_url"]
