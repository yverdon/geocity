from datetime import timedelta
from decimal import *

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import SuspiciousOperation
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from geocity.apps.accounts.models import AdministrativeEntity, PermitDepartment
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


class ServiceFeeType(models.Model):
    administrative_entity = models.ForeignKey(
        AdministrativeEntity,
        null=False,
        on_delete=models.CASCADE,
        verbose_name=_("Entité administrative"),
        related_name="administrative_entity",
        help_text=_("Entité administrative."),
    )
    name = models.CharField(
        verbose_name=_("Prestation"),
        max_length=255,
        null=False,
    )
    fix_price = models.DecimalField(
        default=None,
        null=True,  # For hourly service fees, this field has to be null,
        blank=True,
        decimal_places=2,
        max_digits=12,
        verbose_name=_("Tarif forfaitaire [CHF]"),
        help_text=_("Le tarif forfaitaire de cette prestation."),
    )
    fix_price_editable = models.BooleanField(
        verbose_name=_("Montant à saisir manuelllement"),
        help_text=_(
            "Exemple: montant demandant un calcul spécifique à réaliser en dehors de l'application"
        ),
        default=False,
    )
    is_visible_by_validator = models.BooleanField(
        verbose_name=_("Visible par le validateur"),
        help_text=_("Est visible par le validateur"),
        default=False,
    )

    class Meta:
        verbose_name = _("2.4 Type de prestation")
        verbose_name_plural = _("2.4 Types de prestation")

    def __str__(self):
        return f"{self.name}"


class ServiceFee(models.Model):

    # Hidden yet mandatory fields
    # created_* and updated_* fields to keep tracks of the user that has
    # effectively created or updated the current prestation.
    # Those fields SHOULD NOT be exposed in the form.
    # Use the other ones, e.g. provided_*
    created_at = models.DateTimeField(
        verbose_name=_("Date de création."),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Date de dernière modification."),
        auto_now=True,
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        max_length=255,
        verbose_name=_("Créée par"),
        related_name="service_fee_created_by",
        help_text=_("La prestation a été créé par cet utilisateur."),
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        max_length=255,
        verbose_name=_("Mise à jour par"),
        related_name="service_fee_updated_by",
        help_text=_("La prestation a été mise à jour par cet utilisateur."),
    )
    permit_department = models.ForeignKey(
        PermitDepartment,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Département"),
        related_name="permit_department",
        help_text=_("Département."),
    )
    # Exposed fields: fields which can be used in the form based on that model.
    # The "provided_by" field is used to select the name of the user
    # on whose behalf the service was provided.
    provided_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        max_length=255,
        verbose_name=_("Saisie par"),
        related_name="service_fee_provided_by",
        help_text=_("La prestation a été effectuée au nom de cet utilisateur."),
    )
    provided_at = models.DateField(
        default=timezone.now,
        verbose_name=_("Saisie le"),
        help_text=_("La prestation a été saisie à cette date."),
    )
    submission = models.ForeignKey(
        "Submission",
        on_delete=models.CASCADE,
        verbose_name=_("Demande"),
        related_name="service_fee",
        help_text=_("Demande"),
    )
    service_fee_type = models.ForeignKey(
        "ServiceFeeType",
        on_delete=models.CASCADE,
        verbose_name=_("Type de prestation"),
        related_name="service_fee_type",
        help_text=_("Choix de la prestation ; à effectuer dans une liste prédéfinie."),
    )
    time_spent_on_task = models.DurationField(
        default=0,
        null=True,  # For fixed price service fees
        verbose_name=_("Durée [m]"),
        help_text=_("Temps passé pour effectuer la prestation (en minutes)."),
    )
    hourly_rate = models.DecimalField(
        default=settings.DEFAULT_SERVICES_FEES_RATE,
        null=True,  # For fixed price service fees, this field has to be null
        decimal_places=2,
        max_digits=12,
        verbose_name=_("Tarif horaire [CHF]"),
        help_text=_("Le tarif horaire de la prestation. Choisi par l'intégrateur."),
    )
    # The "monetary_amount" field must only be exposed for fixed price service fees
    monetary_amount = models.DecimalField(
        default=0.0,
        decimal_places=2,
        max_digits=12,
        verbose_name=_("Montant [CHF]"),
        help_text=_(
            "Le montant de la prestation. "
            "Calulé automatiquement en fonction du tarif horaire. "
            "Est fixe si la prestation est forfaitaire. "
            "Certains montants fixes peuvent être modifiables lorsque le type de prestation exige un calcul spécifique. "
        ),
    )

    # Methods
    def save(self, *args, **kwargs):
        # For hourly service fees
        if isinstance(self.time_spent_on_task, timedelta):
            # Get service fee hourly rate from the service_fee_type model
            self.hourly_rate = (
                self.service_fee_type.administrative_entity.services_fees_hourly_rate
            )
            # Compute the corresponding monetary amount
            self.monetary_amount = (
                Decimal(self.hourly_rate)
                * Decimal(self.time_spent_on_task.total_seconds())
                / Decimal(3600)
            )
        # For fixed price service fees
        else:
            self.hourly_rate = None
            self.time_spent_on_task = None

        super(ServiceFee, self).save(*args, **kwargs)
