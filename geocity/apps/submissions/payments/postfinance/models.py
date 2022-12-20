from simple_history.models import HistoricalRecords

from geocity.apps.submissions.payments.models import Transaction


class PostFinanceTransaction(Transaction):
    CHECKOUT_PROCESSOR_ID = "PostFinance"
    history = HistoricalRecords()
