from django.core.exceptions import SuspiciousOperation
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from geocity.apps.forms.models import Price
from geocity.apps.reports.services import generate_report_pdf


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
        return self.transactions.all()


class Transaction(models.Model):
    CHECKOUT_PROCESSOR_ID = None
    STATUS_UNPAID = "unpaid"
    STATUS_PAID = "paid"
    STATUS_TO_REFUND = "to_refund"
    STATUS_REFUNDED = "refunded"
    STATUS_FAILED = "failed"
    TYPE_SUBMISSION = "submission"
    TYPE_PROLONGATION = "prolongation"
    submission_price = models.ForeignKey(
        "SubmissionPrice",
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    amount = models.DecimalField(_("Montant"), max_digits=6, decimal_places=2)
    currency = models.CharField(_("Devise"), max_length=20)
    transaction_id = models.CharField(_("ID transaction"), max_length=255)
    status = models.CharField(
        _("Statut"),
        max_length=20,
        choices=[
            (STATUS_UNPAID, _("Pas payée")),
            (STATUS_PAID, _("Payée")),
            (STATUS_TO_REFUND, _("À rembourser")),
            (STATUS_REFUNDED, _("Remboursée")),
            (STATUS_FAILED, _("Échouée")),
        ],
        default=STATUS_UNPAID,
    )
    creation_date = models.DateTimeField(_("Date de création"), auto_now_add=True)
    updated_date = models.DateTimeField(_("Date de modification"), auto_now=True)
    authorization_timeout_on = models.DateTimeField(
        _("Date de fin d'authorisation"), null=True
    )
    payment_url = models.CharField(_("URL de paiement"), max_length=255, null=True)

    transaction_type = models.CharField(
        _("Type de transaction"),
        choices=[
            (TYPE_SUBMISSION, _("Soumission")),
            (TYPE_PROLONGATION, _("Prolongation")),
        ],
        max_length=20,
        default=TYPE_SUBMISSION,
    )

    class Meta:
        abstract = True
        ordering = ("-creation_date",)

    @property
    def can_have_status_changed(self):
        return self.amount > 0

    def set_refunded(self):
        self.status = self.STATUS_REFUNDED
        self.save()

    def set_paid(self):
        self.status = self.STATUS_PAID
        self.save()

    def set_to_refund(self):
        self.status = self.STATUS_TO_REFUND
        self.save()

    def set_failed(self):
        self.status = self.STATUS_FAILED
        self.save()

    def set_new_status(self, new_status):
        return {
            self.STATUS_TO_REFUND: self.set_to_refund,
            self.STATUS_REFUNDED: self.set_refunded,
            self.STATUS_PAID: self.set_paid,
        }[new_status]()

    def requires_action_on_merchant_site(self, new_status):
        return new_status in (self.STATUS_REFUNDED, self.STATUS_PAID)

    def get_confirmation_pdf(self, read=False):
        submission = self.submission_price.submission
        form = submission.get_form_for_payment()
        if not form or not form.payment_settings:
            raise SuspiciousOperation
        payment_settings = form.payment_settings
        report = payment_settings.payment_confirmation_report
        output = generate_report_pdf(
            submission.author, submission.pk, form.pk, report.pk, self.pk
        )
        if read:
            output = output.read()
        return f"invoice_{self.transaction_id}.pdf", output

    def get_refund_pdf(self, read=False):
        submission = self.submission_price.submission
        form = submission.get_form_for_payment()
        if not form or not form.payment_settings:
            raise SuspiciousOperation
        payment_settings = form.payment_settings
        report = payment_settings.payment_refund_report
        output = generate_report_pdf(
            submission.author, submission.pk, form.pk, report.pk, self.pk
        )
        if read:
            output = output.read()
        return f"refund_{self.transaction_id}.pdf", output
