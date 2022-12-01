from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from geocity.apps.forms.models import Price


class SubmissionPrice(models.Model):
    submission = models.OneToOneField(
        "Submission", related_name="price", on_delete=models.CASCADE
    )
    original_price = models.ForeignKey(Price, on_delete=models.SET_NULL, null=True)
    text = models.CharField(_("Texte"), max_length=255)
    amount = models.DecimalField(_("Montant"), max_digits=6, decimal_places=2)
    currency = models.CharField(_("Devise"), max_length=20)
    history = HistoricalRecords()

    def get_transactions(self):
        return self.postfinancetransaction_set.all()


class Transaction(models.Model):
    CHECKOUT_PROCESSOR_ID = None
    STATUS_UNPAID = "unpaid"
    STATUS_PAID = "paid"
    STATUS_TO_REFUND = "to_refund"
    STATUS_REFUNDED = "refunded"
    submission_price = models.ForeignKey("SubmissionPrice", on_delete=models.CASCADE)
    amount = models.DecimalField(_("Montant"), max_digits=6, decimal_places=2)
    currency = models.CharField(_("Devise"), max_length=20)
    merchant_reference = models.CharField(_("Référence marchande"), max_length=255)
    status = models.CharField(
        _("Statut"),
        max_length=20,
        choices=[
            (STATUS_UNPAID, _("Pas payé")),
            (STATUS_PAID, _("Payé")),
            (STATUS_TO_REFUND, _("À rembourser")),
            (STATUS_REFUNDED, _("Remboursé")),
        ],
        default=STATUS_UNPAID,
    )
    creation_date = models.DateTimeField(_("Date de création"), auto_now_add=True)
    updated_date = models.DateTimeField(_("Date de modification"), auto_now=True)

    class Meta:
        abstract = True

    def set_refunded(self):
        self.status = self.STATUS_REFUNDED
        self.save()

    def set_paid(self):
        self.status = self.STATUS_PAID
        self.save()

    def set_to_refund(self):
        self.status = self.STATUS_TO_REFUND
        self.save()

    def set_new_status(self, new_status):
        return {
            self.STATUS_TO_REFUND: self.set_to_refund,
            self.STATUS_REFUNDED: self.set_refunded,
            self.STATUS_PAID: self.set_paid,
        }[new_status]()
