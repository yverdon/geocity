import collections
import uuid

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
    validate_slug,
)
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django_jsonform.models.fields import JSONField
from simple_history.models import HistoricalRecords
from taggit.managers import TaggableManager

from geocity.apps.accounts.fields import AdministrativeEntityFileField
from geocity.apps.accounts.models import AdministrativeEntity
from geocity.apps.api.services import convert_string_to_api_key
from geocity.apps.reports.models import Report

from . import fields


class FormCategoryQuerySet(models.QuerySet):
    def filter_by_tags(self, tags):
        return self.filter(tags__name__in=[tag.lower() for tag in tags])


class FormCategory(models.Model):
    name = models.CharField(_("nom"), max_length=255)

    META_TYPE_OTHER = 0
    META_TYPE_ROADWORK = 1
    META_TYPE_BUILDINGWORK = 2
    META_TYPE_EVENT_SPORT = 3
    META_TYPE_EVENT_CULTURE = 4
    META_TYPE_EVENT_COMMERCIAL = 5
    META_TYPE_EVENT_POLICE = 6
    META_TYPE_CHOICES = (
        (META_TYPE_OTHER, _("Autres")),
        (META_TYPE_ROADWORK, _("Chantier")),
        (META_TYPE_BUILDINGWORK, _("Construction")),
        (META_TYPE_EVENT_SPORT, _("Événement sportif")),
        (META_TYPE_EVENT_CULTURE, _("Événement culturel")),
        (META_TYPE_EVENT_COMMERCIAL, _("Événement commercial")),
        (META_TYPE_EVENT_POLICE, _("Dispositif de police")),
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
        limit_choices_to={"permit_department__is_integrator_admin": True},
    )
    meta_type = models.IntegerField(
        _("Type générique"), choices=META_TYPE_CHOICES, default=META_TYPE_OTHER
    )
    tags = TaggableManager(
        blank=True,
        verbose_name="Mots-clés",
        help_text="Mots clefs sans espaces, séparés par des virgules permettant de filtrer les types par l'url: https://geocity.ch/?typefilter=stationnement",
    )
    objects = FormCategoryQuerySet().as_manager()

    class Meta:
        verbose_name = _("1.2 Catégorie")
        verbose_name_plural = _("1.2 Catégories")

    def __str__(self):
        return self.name


class AnonymousFormManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_anonymous=True)


class FormQuerySet(models.QuerySet):
    def get_default_forms(
        self,
        administrative_entity,
        user,
        limit_to_categories=None,
    ):
        """
        Return the `Form` that should be automatically selected for the given
        `administrative_entity`. `form_categories` should be the categories the user has
        selected, if any.
        """
        forms = self.filter(administrative_entities=administrative_entity)

        if not user.has_perm("submissions.view_private_form"):
            forms = forms.filter(is_public=True)

        if limit_to_categories:
            forms = forms.filter(category__in=limit_to_categories)

        if len(forms) > 1:
            return Form.objects.none()

        return forms

    def get_administrative_entities_with_forms(self, user, site=None):
        """Default queryset, for integrator, can fill all forms except anonymous ones"""
        queryset = (
            AdministrativeEntity.objects.filter(
                pk__in=self.values_list("administrative_entities", flat=True),
                forms__is_anonymous=False,
            )
            .order_by("ofs_id", "name")
            .distinct()
        )

        if site:
            queryset = queryset.filter(sites=site)

        integrator_admin = user.groups.filter(
            permit_department__is_integrator_admin=True
        ).first()

        user_administrative_entities = AdministrativeEntity.objects.associated_to_user(
            user
        )

        user_can_view_private_form = user.has_perm("submissions.view_private_form")

        if not user.is_superuser:
            if integrator_admin:
                """An integrator can fill all forms he owns + public ones"""
                queryset = queryset.filter(
                    Q(integrator=integrator_admin) | Q(forms__is_public=True)
                )
            elif user_administrative_entities and user_can_view_private_form:
                """User is trusted and associated to administrative entities,
                he can fill private forms for those administrative entities
                if granted permission 'view_private_form'"""
                queryset = queryset.filter(
                    Q(pk__in=user_administrative_entities) | Q(forms__is_public=True)
                )
            elif not user_can_view_private_form or not user_administrative_entities:
                """Untrusted users or user not granted with view_private_form can only fill public forms"""
                queryset = queryset.filter(
                    Q(integrator=integrator_admin) | Q(forms__is_public=True)
                )
            elif user_administrative_entities and user.has_perm(
                "submissions.view_private_form"
            ):
                """User is trusted and associated to administrative entities,
                he can fill private forms for those administrative entities
                if granted permission 'view_private_form'"""
                queryset = queryset.filter(
                    Q(pk__in=user_administrative_entities) | Q(forms__is_public=True)
                )
            elif not user_can_view_private_form or not user_administrative_entities:
                """Untrusted users or user not granted with view_private_form can only fill public forms"""
                queryset = queryset.filter(forms__is_public=True)

        return queryset


def default_currency():
    return settings.PAYMENT_CURRENCY


class PaymentSettings(models.Model):
    name = models.CharField(_("Nom des paramètres"), max_length=255)
    prices_label = models.CharField(
        _("Label pour les tarifs"),
        max_length=255,
        default=_("Tarifs"),
        help_text=_(
            "Texte affiché à l'utilisateur comme en-têtes des prix (p. ex.: 'Tarifs')"
        ),
    )
    internal_account = models.CharField(
        _("Compte interne"),
        max_length=255,
        help_text=_("Compte interne de comptabilité utilisé pour les paiements"),
    )
    payment_processor = models.CharField(
        _("Processeur de paiement"),
        max_length=255,
        choices=[
            ("PostFinance", "PostFinance Checkout"),
        ],
        default="PostFinance",
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
        limit_choices_to={"permit_department__is_integrator_admin": True},
    )
    space_id = models.CharField(_("Space ID"), max_length=255, null=False)
    user_id = models.CharField(_("User ID"), max_length=255, null=False)
    api_key = models.CharField(_("API key"), max_length=255, null=False)

    payment_confirmation_report = models.ForeignKey(
        Report,
        null=True,
        on_delete=models.PROTECT,
        related_name="confirmation_payment_settings_objects",
        verbose_name=_("Rapport pour la confirmation des paiements"),
    )
    payment_refund_report = models.ForeignKey(
        Report,
        null=True,
        on_delete=models.PROTECT,
        related_name="refund_payment_settings_objects",
        verbose_name=_("Rapport pour le remboursement des paiements"),
    )

    def __str__(self):
        return f"{self.name} - {self.internal_account}"

    class Meta:
        verbose_name = _("1.6 Paramètres de paiement")
        verbose_name_plural = _("1.6 Paramètres de paiement")

    def clean(self):
        if self.payment_confirmation_report is not None and self.pk is not None:
            for form in self.form_set.all():
                has_doc_types_with_form = (
                    self.payment_confirmation_report.document_types.filter(
                        parent__form=form.pk
                    )
                )
                if not has_doc_types_with_form:
                    raise ValidationError(
                        {
                            "payment_confirmation_report": _(
                                f"Il faut ajouter une catégorie de document liée à {form.name} dans le modèle d'impression {self.payment_confirmation_report.name}"
                            )
                        }
                    )
        if self.payment_refund_report is not None and self.pk is not None:
            for form in self.form_set.all():
                has_doc_types_with_form = (
                    self.payment_refund_report.document_types.filter(
                        parent__form=form.pk
                    )
                )
                if not has_doc_types_with_form:
                    raise ValidationError(
                        {
                            "payment_refund_report": _(
                                f"Il faut ajouter une catégorie de document liée à {form.name} dans le modèle d'impression {self.payment_refund_report.name}"
                            )
                        }
                    )


class Price(models.Model):
    text = models.CharField(_("Texte"), max_length=255)
    amount = models.DecimalField(
        _("Montant"),
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_("Un montant de 0 peut être utilisé pour avoir un tarif gratuit"),
    )
    currency = models.CharField(_("Devise"), max_length=20, default=default_currency)
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
        limit_choices_to={"permit_department__is_integrator_admin": True},
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.text} - {self.amount:6.2f} {self.currency}"

    def str_for_choice(self):
        return mark_safe(
            f"<strong>{self.text}</strong> - {self.amount:6.2f} {self.currency}"
        )

    class Meta:
        verbose_name = _("1.7 Tarif")
        verbose_name_plural = _("1.7 Tarifs")


class FormPrice(models.Model):
    price = models.ForeignKey(
        "Price", on_delete=models.CASCADE, verbose_name=_("Tarif")
    )
    form = models.ForeignKey(
        "Form", on_delete=models.CASCADE, verbose_name=_("Formulaire")
    )

    order = models.PositiveSmallIntegerField(
        _("Position dans les tarifs"), default=0, db_index=True
    )

    class Meta:
        unique_together = ("price", "form")
        ordering = ("order", "price")


class MapWidgetConfiguration(models.Model):
    ITEMS_SCHEMA = {
        "type": "object",
        "keys": {
            "mode": {
                "type": "object",
                "keys": {
                    "type": {
                        "type": "string",
                        "title": "Modes d’interaction avec la carte",
                        "choices": [
                            {
                                "title": "Création",
                                "value": "create",
                            },
                            {"title": "Sélection", "value": "select"},
                            {"title": "Cible", "value": "target"},
                            {"title": "Mixte", "value": "mix"},
                        ],
                        "widget": "radio",
                    }
                },
            },
        },
    }
    name = models.CharField(_("Nom de la configuration"), max_length=255)
    configuration = JSONField(schema=ITEMS_SCHEMA)
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
        limit_choices_to={"permit_department__is_integrator_admin": True},
    )

    class Meta:
        verbose_name = _("1.8 Module cartographique avancé")
        verbose_name_plural = _("1.8 Modules cartographiques avancés")

    def __str__(self):
        return self.name


class Form(models.Model):
    """
    Represents a Form configuration object.
    """

    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
        limit_choices_to={"permit_department__is_integrator_admin": True},
    )
    category = models.ForeignKey(
        FormCategory,
        on_delete=models.CASCADE,
        verbose_name=_("catégorie"),
        related_name="forms",
    )
    administrative_entities = models.ManyToManyField(
        AdministrativeEntity,
        verbose_name=_("entité administrative"),
        related_name="forms",
    )
    can_always_update = models.BooleanField(
        _("Demande modifiable en tout temps par le secrétariat"), default=False
    )
    can_have_multiple_ranges = models.BooleanField(
        _("Peut avoir plusieurs plages"), default=False
    )
    has_geometry_point = models.BooleanField(_("Point"), default=True)
    has_geometry_line = models.BooleanField(_("Ligne"), default=True)
    has_geometry_polygon = models.BooleanField(_("Surface"), default=True)
    directive = AdministrativeEntityFileField(
        _("directive"),
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        blank=True,
    )
    directive_description = models.CharField(
        _("description de la directive"), max_length=200, blank=True
    )
    additional_information = models.TextField(_("autre information"), blank=True)
    needs_date = models.BooleanField(_("avec période de temps"), default=True)
    start_delay = models.IntegerField(
        _("délai de commencement"),
        blank=True,
        null=True,
        help_text=_(
            "Délai minimum en jours avant la date de début "
            "(nombre entier positif ou négatif)."
        ),
    )
    requires_payment = models.BooleanField(
        _("Demande soumise à des frais"), default=True
    )

    requires_online_payment = models.BooleanField(
        _("Soumis au paiement en ligne"),
        default=False,
        help_text=mark_safe(
            _(
                "Requiert la présence de <strong>paramètres de paiement</strong>, "
                "d'au moins un <strong>tarif</strong>, et de <strong>ne pas être "
                "soumis à des frais</strong>."
            )
        ),
    )
    payment_settings = models.ForeignKey(
        "PaymentSettings",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Paramètres de paiement"),
    )

    requires_validation_document = models.BooleanField(
        _("Document de validation obligatoire"), default=True
    )
    # TODO: sphinx documentation, to explain is used to make visible/hidden in the list of forms
    is_public = models.BooleanField(_("Formulaire public"), default=False)
    is_anonymous = models.BooleanField(
        _("Demandes anonymes uniquement"),
        default=False,
    )
    notify_services = models.BooleanField(_("Notifier les services"), default=False)
    services_to_notify = models.TextField(
        _("Emails des services à notifier"),
        blank=True,
        help_text='Veuillez séparer les emails par une virgule ","',
    )
    permit_duration = models.IntegerField(
        _("Durée de validité de la demande (jours)"),
        blank=True,
        null=True,
        help_text=_(
            "Le permis pour l'objet sera prolongeable uniquement si cette valeur est fournie."
        ),
    )
    expiration_reminder = models.BooleanField(
        _("Activer la fonction de rappel"),
        default=False,
    )
    days_before_reminder = models.IntegerField(
        _("Délai de rappel (jours)"), blank=True, null=True
    )
    document_enabled = models.BooleanField(
        _("Activer la gestion des documents"), default=False
    )
    publication_enabled = models.BooleanField(
        _("Activer la gestion de la publication"), default=False
    )
    permanent_publication_enabled = models.BooleanField(
        _("Autoriser la mise en consultation sur une durée indéfinie"), default=False
    )
    shortname = models.CharField(
        _("nom court"),
        max_length=32,
        help_text=_(
            "Nom affiché par défaut dans les différentes étapes du formulaire, ne s'affiche pas dans l'admin (max. 32 caractères)"
        ),
        blank=True,
    )

    name = models.CharField(_("nom"), max_length=255)
    api_name = models.CharField(
        _("Nom dans l'API"),
        max_length=255,
        blank=True,
        help_text=_("Se génère automatiquement lorsque celui-ci est vide."),
    )
    order = models.PositiveIntegerField(
        _("ordre"), default=0, blank=False, null=False, db_index=True
    )
    wms_layers = models.URLField(_("Couche(s) WMS"), blank=True, max_length=1024)
    wms_layers_order = models.PositiveIntegerField(
        _("Ordre de(s) couche(s)"), default=1
    )
    prices = models.ManyToManyField(
        "Price", verbose_name=_("tarifs"), related_name="forms", through=FormPrice
    )
    max_submissions = models.PositiveIntegerField(
        _("Nombre maximum de demandes"), null=True, blank=True
    )
    max_submissions_message = models.CharField(
        _("Message lorsque le nombre maximal est atteint"),
        max_length=300,
        default=_(
            "Ce formulaire est désactivé car le nombre maximal de soumissions a été atteint."
        ),
        null=True,
        blank=True,
    )
    max_submissions_bypass_enabled = models.BooleanField(
        _(
            "Autoriser le secrétariat à soumettre des demandes même si le nombre maximal est atteint"
        ),
        default=False,
    )
    GEO_WIDGET_GENERIC = 1
    GEO_WIDGET_ADVANCED = 2
    GEO_WIDGET_CHOICES = (
        (GEO_WIDGET_GENERIC, _("Générique")),
        (GEO_WIDGET_ADVANCED, _("Avancée")),
    )
    geo_widget_option = models.IntegerField(
        _("Choix de l'interface de saisie cartographique"),
        choices=GEO_WIDGET_CHOICES,
        default=GEO_WIDGET_GENERIC,
    )
    map_widget_configuration = models.ForeignKey(
        MapWidgetConfiguration,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="map_widget_configuration_form",
        verbose_name=_("Configuration de la carte avancée"),
    )
    quick_access_slug = models.TextField(
        blank=True,
        default=uuid.uuid4,
        unique=True,
        validators=[validate_slug],
        verbose_name=_("URL courte"),
        help_text=_(
            """Permettant d'accéder directement au formulaire par l'url: https://geocity.ch/?form=URL_COURTE<br>
            Pour une demande anonyme https://geocity.ch/submissions/anonymous/?form=URL_COURTE"""
        ),
    )
    agenda_visible = models.BooleanField(
        _("Visible dans l'agenda"),
        default=False,
        help_text=_(
            """Lorsque cette case est cochée, les données de ce formulaire sont accessibles dans l'API <b>/rest/agenda/ si la demande est rendue publique par le pilote</b><br>
            Le pilote peut alors contrôler la publication dans l'agenda dans l'onglet traitement"""
        ),
    )
    disable_validation_by_validators = models.BooleanField(
        _("Désactiver la validation par les services"), default=False
    )

    # All objects
    objects = FormQuerySet().as_manager()

    # Only anonymous objects
    anonymous_objects = AnonymousFormManager()

    class Meta:
        verbose_name = _("1.4 Formulaire")
        verbose_name_plural = _("1.4 Formulaires")
        ordering = ("order",)

    def __str__(self):
        return self.name

    @property
    def has_geometry(self):
        return (
            self.has_geometry_point
            or self.has_geometry_line
            or self.has_geometry_polygon
        )

    @property
    def nb_submissions_taken_into_account_for_max_submissions(self):
        from ..submissions.models import Submission
        from ..submissions.payments.models import Transaction

        # Submissions taken into account for the maximum number of submissions:
        # - All submissions that are not in statuses draft, rejected or archived
        #   (i.e. submitted)
        # - All submissions that have a transaction that is unpaid and not expired
        #   (i.e. user is in the process of paying, but hasn't finished yet)

        return (
            self.submissions.filter(
                ~Q(
                    status__in=[
                        Submission.STATUS_DRAFT,
                        Submission.STATUS_REJECTED,
                        Submission.STATUS_ARCHIVED,
                    ]
                )
                | Q(
                    price__transactions__authorization_timeout_on__gt=now(),
                    price__transactions__status=Transaction.STATUS_UNPAID,
                )
            )
            .distinct()
            .count()
        )

    def has_exceeded_maximum_submissions(self, user_for_bypass=None):
        from ..submissions.permissions import has_permission_to_amend_submission_in_form

        has_exceeded = (
            self.max_submissions
            and self.nb_submissions_taken_into_account_for_max_submissions
            >= self.max_submissions
        )

        if has_exceeded and self.max_submissions_bypass_enabled and user_for_bypass:
            return not has_permission_to_amend_submission_in_form(user_for_bypass, self)

        return has_exceeded

    def clean(self):
        from geocity.apps.submissions.models import Submission

        if self.max_submissions is not None and self.max_submissions < 1:
            raise ValidationError(
                {
                    "max_submissions": _(
                        "Le nombre maximum de demandes doit être supérieur à 0."
                    )
                }
            )
        if bool(self.directive_description) ^ bool(self.directive):
            raise ValidationError(
                {
                    "directive_description": _(
                        "La description de directive ne devrait pas être définie car cet objet n’a pas de directive associée."
                    )
                    if not self.directive
                    else _("Ce champ est obligatoire lorsqu’une directive est définie.")
                }
            )

        if (
            self.requires_online_payment
            and not self.administrative_entities.first().is_single_form_submissions
        ):
            raise ValidationError(
                {
                    "requires_online_payment": _(
                        "Ne peut pas être coché, car l'entité administrative accepte "
                        "les demandes sur plusieurs objets."
                    )
                }
            )

        if self.requires_online_payment and not self.payment_settings:
            raise ValidationError(
                {
                    "requires_online_payment": _(
                        "Nécessite que des paramètres de paiement soient sélectionnés."
                    )
                }
            )

        if self.requires_online_payment and self.requires_payment:
            raise ValidationError(
                {
                    "requires_online_payment": mark_safe(
                        _(
                            "Les demandes <strong>soumises à des frais</strong> ne peuvent "
                            "pas offrir le <strong>paiement en ligne</strong>. "
                            "Veuillez choisir une des deux options."
                        )
                    )
                }
            )
        if (
            self.requires_online_payment
            and settings.SESSION_COOKIE_SAMESITE.lower() != "lax"
        ):
            raise ValidationError(
                {
                    "requires_online_payment": mark_safe(
                        _(
                            """Cette instance de Geocity n'est pas configurée correctement pour le
                            paiement en ligne. <strong>SESSION_COOKIE_SAMESITE</strong> doit être <strong>Lax</strong>"""
                        )
                    )
                }
            )

        if self.requires_online_payment and not self.prices.exists():
            raise ValidationError(
                {
                    "requires_online_payment": mark_safe(
                        _("Nécessite l'existence d'au moins un <strong>tarif</strong>.")
                    )
                }
            )
        if self.payment_settings:
            conf_report = self.payment_settings.payment_confirmation_report
            refund_report = self.payment_settings.payment_refund_report

            if conf_report:
                has_doc_types_with_conf_report = conf_report.document_types.filter(
                    parent__form=self.pk
                )
                if not has_doc_types_with_conf_report.exists():
                    raise ValidationError(
                        {
                            "payment_settings": _(
                                f"Il faut ajouter une catégorie de document liée à {self.name} dans le modèle d'impression {conf_report.name}"
                            )
                        }
                    )
            if refund_report:
                has_doc_types_with_refund_report = refund_report.document_types.filter(
                    parent__form=self.pk
                )
                if not has_doc_types_with_refund_report.exists():
                    raise ValidationError(
                        {
                            "payment_settings": _(
                                f"Il faut ajouter une catégorie de document liée à {self.name} dans le modèle d'impression {refund_report.name}"
                            )
                        }
                    )
        if (
            self.geo_widget_option == self.GEO_WIDGET_ADVANCED
            and not self.administrative_entities.first().is_single_form_submissions
        ):
            url = reverse(
                "admin:forms_administrativeentityforadminsite_change",
                kwargs={"object_id": self.administrative_entities.first().pk},
            )

            raise ValidationError(
                {
                    "geo_widget_option": mark_safe(
                        _(
                            f'L\'option "Autoriser uniquement un objet par demande" doit être cochée sur <a href="{url}" target="_blank"><b>l\'entité administrative</b></a> pour activer ce paramètre'
                        )
                    )
                }
            )

        if self.api_name:
            if self.api_name != convert_string_to_api_key(self.api_name):
                raise ValidationError(
                    {
                        "api_name": _(
                            f"Celui-ci ne peut pas comporter d'espaces ou de caractères spéciaux"
                        )
                    }
                )
        else:
            self.api_name = convert_string_to_api_key(self.name)

        if (
            self.disable_validation_by_validators
            and Submission.objects.filter(
                status__in=[
                    Submission.STATUS_SUBMITTED_FOR_VALIDATION,
                    Submission.STATUS_AWAITING_VALIDATION,
                ],
                forms__pk=self.pk,
            ).exists()
        ):
            raise ValidationError(
                {
                    "disable_validation_by_validators": _(
                        "Impossible de désactiver la validation tant que des demandes liées à ce formulaire sont en attente ou en cours de validation."
                    )
                }
            )


class FormField(models.Model):
    form = models.ForeignKey(Form, related_name="+", on_delete=models.CASCADE)
    field = models.ForeignKey(
        "Field",
        related_name="form_fields",
        on_delete=models.CASCADE,
        verbose_name=_("Champ"),
    )
    order = models.PositiveSmallIntegerField(
        _("Position dans le formulaire"), default=0, db_index=True
    )

    class Meta:
        verbose_name = _("Champ du formulaire")
        verbose_name_plural = _("Champs du formulaire")
        ordering = ("order",)


# Input types
INPUT_TYPE_ADDRESS = "address"
INPUT_TYPE_CHECKBOX = "checkbox"
INPUT_TYPE_DATE = "date"
INPUT_TYPE_FILE = "file"
INPUT_TYPE_FILE_DOWNLOAD = "file_download"
INPUT_TYPE_LIST_MULTIPLE = "list_multiple"
INPUT_TYPE_LIST_SINGLE = "list_single"
INPUT_TYPE_NUMBER = "number"
INPUT_TYPE_REGEX = "regex"
INPUT_TYPE_TEXT = "text"
DISPLAY_TEXT = "text_output"
DISPLAY_TITLE = "title_output"


class Field(models.Model):
    INPUT_TYPE_TEXT = INPUT_TYPE_TEXT
    INPUT_TYPE_CHECKBOX = INPUT_TYPE_CHECKBOX
    INPUT_TYPE_NUMBER = INPUT_TYPE_NUMBER
    INPUT_TYPE_FILE = INPUT_TYPE_FILE
    INPUT_TYPE_FILE_DOWNLOAD = INPUT_TYPE_FILE_DOWNLOAD
    INPUT_TYPE_ADDRESS = INPUT_TYPE_ADDRESS
    INPUT_TYPE_DATE = INPUT_TYPE_DATE
    INPUT_TYPE_REGEX = INPUT_TYPE_REGEX
    INPUT_TYPE_LIST_SINGLE = INPUT_TYPE_LIST_SINGLE
    INPUT_TYPE_LIST_MULTIPLE = INPUT_TYPE_LIST_MULTIPLE
    DISPLAY_TEXT = DISPLAY_TEXT
    DISPLAY_TITLE = DISPLAY_TITLE

    # The choices are sorted according to their values
    INPUT_TYPE_CHOICES = (
        (INPUT_TYPE_ADDRESS, _("Adresse")),
        (INPUT_TYPE_CHECKBOX, _("Case à cocher")),
        (INPUT_TYPE_LIST_MULTIPLE, _("Choix multiple")),
        (INPUT_TYPE_LIST_SINGLE, _("Choix simple")),
        (INPUT_TYPE_DATE, _("Date")),
        (INPUT_TYPE_FILE, _("Fichier")),
        (INPUT_TYPE_FILE_DOWNLOAD, _("Fichier (à télécharger)")),
        (INPUT_TYPE_NUMBER, _("Nombre")),
        (INPUT_TYPE_TEXT, _("Texte")),
        (INPUT_TYPE_REGEX, _("Texte (regex)")),
        (DISPLAY_TEXT, _("Texte à afficher")),
        (DISPLAY_TITLE, _("Titre à afficher")),
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
        limit_choices_to={"permit_department__is_integrator_admin": True},
    )
    name = models.CharField(_("nom"), max_length=255)
    api_name = models.CharField(
        _("Nom dans l'API"),
        max_length=255,
        blank=True,
        help_text=_("Se génère automatiquement lorsque celui-ci est vide."),
    )
    placeholder = models.CharField(
        _("exemple de donnée à saisir"), max_length=255, blank=True
    )
    help_text = models.CharField(
        _("information complémentaire"), max_length=255, blank=True
    )
    input_type = models.CharField(
        _("type de caractéristique"), max_length=30, choices=INPUT_TYPE_CHOICES
    )
    line_number_for_textarea = models.PositiveIntegerField(
        _("Nombre de lignes de la zone de texte"),
        blank=True,
        default=1,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(50)],
    )
    is_mandatory = models.BooleanField(_("obligatoire"), default=False)
    forms = models.ManyToManyField(
        Form, verbose_name=_("objets"), related_name="fields", through=FormField
    )
    choices = models.TextField(
        verbose_name=_("valeurs à choix"),
        blank=True,
        help_text=_("Entrez un choix par ligne"),
    )
    regex_pattern = models.CharField(
        _("regex pattern"),
        max_length=255,
        blank=True,
        help_text=_("Exemple: ^[0-9]{4}$"),
    )
    services_to_notify = models.TextField(
        _("Emails des services à notifier"),
        blank=True,
        help_text='Veuillez séparer les emails par une virgule ","',
    )
    message_for_notified_services = models.CharField(
        _("Message transmis aux services notifiés"),
        max_length=255,
        blank=True,
    )
    file_download = fields.FormFileField(
        _("Fichier"),
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        blank=True,
        # TODO this name is historical because the Form model used to be call WorksObjectType
        # This should be renamed someday and the files in `wot_files` should be moved
        upload_to="wot_files",
    )
    additional_searchtext_for_address_field = models.CharField(
        _("Filtre additionnel pour la recherche d'adresse"),
        max_length=255,
        blank=True,
        help_text=_(
            'Ex: "Yverdon-les-Bains" afin de limiter les recherches à Yverdon, <a href="https://api3.geo.admin.ch/services/sdiservices.html#search" target="_blank">Plus d\'informations</a>'
        ),
    )
    store_geometry_for_address_field = models.BooleanField(
        _("Stocker la géométrie de l'adresse dans la table géométrique"),
        default=False,
        help_text=_(
            "L'API Geoadmin est utilisée afin de trouver un point correspondant à l'adresse. En cas d'échec, le centroïde de l'entité administrative est utilisée <a href=\"https://api3.geo.admin.ch/services/sdiservices.html#search\" target=\"_blank\">Plus d'informations</a>"
        ),
    )
    public_if_submission_public = models.BooleanField(
        _("Information publique"),
        default=False,
        help_text=_(
            """Lorsque cette case est cochée, ce champ est affiché <b>si la demande est rendue publique par le pilote</b>.<br>
            Actuellement utilisé pour l'application geocalendrier et agenda"""
        ),
    )
    allowed_file_types = models.CharField(
        _("Restreindre plus finement les extensions autorisées"),
        max_length=255,
        blank=True,
        help_text=_('Ex: "pdf, jpg, png"'),
    )
    api_light = models.BooleanField(
        _("Visible dans l'API light"),
        default=False,
        help_text=_(
            """Lorsque cette case est cochée, ce champ est affiché dans la version light de l'api (/rest/RESSOURCE) <b>si la demande est rendue publique par le pilote</b>.<br>
            Afin de ne pas afficher trop d'informations, le champ est masqué pour améliorer la rapidité de l'API.<br>
            Pour afficher la version normale de l'api, il faut se rendre sur une seule ressource (/rest/RESSOURCE/:ID)."""
        ),
    )
    filter_for_api = models.BooleanField(
        _("Filtre pour API"),
        default=False,
        help_text=_(
            """Lorsque cette case est cochée, ce champ peut être utilisé pour filtrer <b>si la demande est rendue publique par le pilote</b>.<br>
            Actuellement ne fonctionne que pour les champs à choix simple ou multiples dans agenda."""
        ),
    )

    class Meta(object):
        verbose_name = _("1.3 Champ")
        verbose_name_plural = _("1.3 Champs")
        constraints = [
            models.CheckConstraint(
                check=~(
                    Q(input_type__in=[INPUT_TYPE_LIST_SINGLE, INPUT_TYPE_LIST_MULTIPLE])
                    & Q(choices="")
                ),
                name="field_choices_not_empty_for_lists",
            ),
            models.CheckConstraint(
                check=~(Q(input_type=INPUT_TYPE_REGEX) & Q(regex_pattern="")),
                name="field_pattern_not_empty_for_regex",
            ),
        ]
        indexes = [models.Index(fields=["input_type"])]

    def __str__(self):
        return self.name

    def is_value_field(self):
        return self.input_type in [
            Field.INPUT_TYPE_TEXT,
            Field.INPUT_TYPE_CHECKBOX,
            Field.INPUT_TYPE_NUMBER,
            Field.INPUT_TYPE_FILE,
            Field.INPUT_TYPE_ADDRESS,
            Field.INPUT_TYPE_DATE,
            Field.INPUT_TYPE_LIST_SINGLE,
            Field.INPUT_TYPE_LIST_MULTIPLE,
            Field.INPUT_TYPE_REGEX,
        ]

    def clean(self):
        if self.input_type in [INPUT_TYPE_LIST_SINGLE, INPUT_TYPE_LIST_MULTIPLE]:
            if not self.choices:
                raise ValidationError({"choices": _("This field is required.")})
            else:
                split_choices = [
                    choice.strip() for choice in self.choices.strip().splitlines()
                ]
                counter = collections.Counter(split_choices)
                duplicates = [choice for choice, count in counter.items() if count > 1]

                if duplicates:
                    raise ValidationError(
                        {
                            "choices": _(
                                "Les valeurs suivantes apparaissent plusieurs fois dans la liste : {} "
                            ).format(", ".join(duplicates))
                        }
                    )

                self.choices = "\n".join(split_choices)
        else:
            self.choices = ""

        if self.input_type == INPUT_TYPE_REGEX:
            if not self.regex_pattern:
                raise ValidationError({"regex_pattern": _("This field is required.")})

        if self.api_name:
            if self.api_name != convert_string_to_api_key(self.api_name):
                raise ValidationError(
                    {
                        "api_name": _(
                            f"Celui-ci ne peut pas comporter d'espaces ou de caractères spéciaux"
                        )
                    }
                )
        else:
            self.api_name = convert_string_to_api_key(self.name)
