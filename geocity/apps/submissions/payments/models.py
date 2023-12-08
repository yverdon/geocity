from django.core.exceptions import SuspiciousOperation
from django.db import models
from django.contrib.auth.models import Group, User
from djmoney.models.fields import MoneyField
from django.utils import timezone
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

    class Meta:
        abstract = True
        ordering = ("-creation_date",)

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

class PrestationsType(models.Model):
    name = models.CharField(
        verbose_name=_("Prestation"),
        max_length=255,
        null=False,
    )
    is_visible_by_validator = models.BooleanField(
        verbose_name=_("visible by validator"),
        help_text=_(
            "Est visible par le validateur"
        ),
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
        limit_choices_to={"permit_department__is_integrator_admin": True},
    )
    # Methods
    def __str__(self):
        return f"{self.name}"

class Prestations(models.Model):
    """Docstring
    """
    # Hidden mandatory fields
    # created and updated fields to keep tracks of the user that has effectively
    # created or updated the current prestation. Those fields SHOULD NOT be
    # exposed in the form. Use the other ones.
    created_at = models.DateTimeField(
        verbose_name=_("Date de création."),
        auto_now_add=True,
    )
    updated_at= models.DateTimeField(
        verbose_name=_("Date de dernière modification."),
        auto_now=True,
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        max_length=255,
        verbose_name=_("Créé par"),
        related_name=_("prestations_created_by"),
        help_text=_(
            "La prestation a été créée par cet utilisateur."
        ),
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        max_length=255,
        verbose_name=_("Mis à jour par"),
        related_name=_("prestations_updated_by"),
        help_text=_(
            "La prestation a été mise à jour par cet utilisateur."
        ),
    )
    # Exposed fields to select the name of the user the prestation has been done by
    provided_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        max_length=255,
        verbose_name=_("Saisie par"),
        related_name="prestations_provided_by",
        help_text=_(
            "La prestation a été effectuée au nom de cet utilisateur."
        ),
    )
    provided_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Date de saisie"),
        help_text=_(
            "La prestation a été saisie à cette date."
        ),
    )
    #TODO: GROS TOUT DOUX: créer une FK vers submission
    #ERROR: IMPOSSIBLE TO CREATE A FK: CIRCULAR IMPORT!
    prestation_type =  models.ForeignKey(
        "PrestationsType",
        on_delete=models.CASCADE,
        verbose_name=_("Prestation"),
        related_name=_("prestations_type"),
        help_text=_(
            "Choix de la prestation ; à effectuer dans une liste prédéfinie."
        ),
    )
    time_spent_on_task = models.DurationField(
        default = 0,
        verbose_name=_("Durée [m]"),
        help_text=_(
            "Temps passé pour effectuer la prestation (en minutes)."
        ),
    )
    pricing = MoneyField(
        default=140,
        decimal_places=2,
        max_digits=12,
        default_currency='CHF',
        verbose_name=_("Tarif horaire [CHF]"),
    )
    monetary_amount = MoneyField(
        decimal_places=2,
        max_digits=12,
        default_currency='CHF',
        default=0.0,
        verbose_name=_("Montant [CHF]"),
    )
    # Methods
    def save(self, *args, **kwargs):
        if not self.monetary_amount:
            self.monetary_amount = self.pricing * self.time_spent_on_task.total_seconds()/3600
        
        super(Prestations, self).save(*args, **kwargs)
