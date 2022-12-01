from .postfinance.processor import PostFinanceCheckoutProcessor

PAYMENT_PROCESSING_PROVIDERS = {
    PostFinanceCheckoutProcessor.identifier: PostFinanceCheckoutProcessor
}


def get_payment_processor_class(payment_provider_id):
    """
    Returns a payment processor class from its given provider ID
    """
    return PAYMENT_PROCESSING_PROVIDERS.get(payment_provider_id)


def get_payment_processor(form):
    pay_class = get_payment_processor_class(form.payment_settings.payment_processor)

    kwargs = {}
    for param in pay_class.required_params:
        kwargs[param] = getattr(form.payment_settings, param)
    return pay_class(**kwargs)


def get_transaction_from_merchant_reference(merchant_reference):
    return PostFinanceCheckoutProcessor.transaction_class.objects.get(
        merchant_reference=merchant_reference
    )
