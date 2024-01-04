from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.exceptions import SuspiciousOperation
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
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


class ServicesFeesType(models.Model):
    administrative_entity = models.ForeignKey(
        AdministrativeEntity,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Administrative entity"),
        related_name="administrative_entity",
        help_text=_("Administrative entity."),
    )
    name = models.CharField(
        verbose_name=_("Service fee"),
        max_length=255,
        null=False,
    )
    is_visible_by_validator = models.BooleanField(
        verbose_name=_("visible by validator"),
        help_text=_("Is visible by the validator"),
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Administrators group"),
        limit_choices_to={"permit_department__is_integrator_admin": True},
    )

    # Methods
    def __str__(self):
        return f"{self.name}"


class ServicesFees(models.Model):
    """Docstring"""

    # Hidden mandatory fields
    # created and updated fields to keep tracks of the user that has effectively
    # created or updated the current prestation. Those fields SHOULD NOT be
    # exposed in the form. Use the other ones.
    created_at = models.DateTimeField(
        verbose_name=_("Creation date."),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Last modification date."),
        auto_now=True,
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        max_length=255,
        verbose_name=_("Created by"),
        related_name="service_fee_created_by",
        help_text=_("The service fee was created by this user."),
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        max_length=255,
        verbose_name=_("Updated by"),
        related_name="service_fee_updated_by",
        help_text=_("The service fee was updated by this user."),
    )
    permit_department = models.ForeignKey(
        PermitDepartment,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Departement"),
        related_name="permit_department",
        help_text=_("Departement."),
    )
    # Exposed fields to select the name of the user the prestation has been done by
    provided_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        max_length=255,
        verbose_name=_("Provided by"),
        related_name="service_fee_provided_by",
        help_text=_("The service fee was provided on behalf of this user."),
    )
    provided_at = models.DateField(
        default=timezone.now,
        verbose_name=_("Provided date"),
        help_text=_("The service fee was provided on this date."),
    )
    submission = models.ForeignKey(
        "Submission",
        on_delete=models.CASCADE,
        verbose_name=_("Request"),
        related_name="submission",
        help_text=_("Request"),
    )
    services_fees_type = models.ForeignKey(
        "ServicesFeesType",
        on_delete=models.CASCADE,
        verbose_name=_("Service fee type"),
        related_name="services_fees_type",
        help_text=_("Choice of service; to be selected from a predefined list."),
    )
    time_spent_on_task = models.DurationField(
        default=0,
        verbose_name=_("Duration [m]"),
        help_text=_("Time spent performing the service (in minutes)."),
    )
    pricing = MoneyField(
        default=settings.DEFAULT_SERVICES_FEES_RATE,
        decimal_places=2,
        max_digits=12,
        default_currency="CHF",
        verbose_name=_("Hourly rate [CHF]"),
    )
    monetary_amount = MoneyField(
        decimal_places=2,
        max_digits=12,
        default_currency="CHF",
        default=0.0,
        verbose_name=_("Amount [CHF]"),
    )

    # Methods
    def save(self, *args, **kwargs):
        pricing = self.services_fees_type.administrative_entity.services_fees_rate
        self.pricing = pricing
        if not self.monetary_amount:
            self.monetary_amount = (
                pricing * self.time_spent_on_task.total_seconds() / 3600
            )

        super(ServicesFees, self).save(*args, **kwargs)
