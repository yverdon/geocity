import collections

from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from geocity.apps.accounts.fields import AdministrativeEntityFileField
from geocity.apps.accounts.models import AdministrativeEntity

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
        form_categories=None,
    ):
        """
        Return the `Form` that should be automatically selected for the given
        `administrative_entity`. `form_categories` should be the categories the user has
        selected, if any.
        """
        forms = self.filter(administrative_entities=administrative_entity)

        if not user.has_perm("submissions.see_private_requests"):
            forms = forms.filter(is_public=True)

        if form_categories is not None:
            forms = forms.filter(category__in=form_categories)

        available_forms = {form.pk for form in forms}
        available_categories = {form.category_id for form in forms}

        # If `form_categories` are not set, ie. the user has only selected an administrative
        # entity but no categories yet, and there’s more than 1 category available, don’t
        # return any default forms so the user can choose the categorie(s) first
        if (form_categories is None and len(available_categories) > 1) or len(
            available_forms
        ) > 1:
            return Form.objects.none()

        return forms

    def get_administrative_entities_with_forms(self, user, site=None):
        queryset = (
            AdministrativeEntity.objects.filter(
                pk__in=self.values_list("administrative_entities", flat=True),
                forms__is_anonymous=False,
            )
            .order_by("ofs_id", "-name")
            .distinct()
        )

        if site:
            queryset = queryset.filter(sites=site)

        if not user.has_perm("submissions.see_private_requests"):
            queryset = queryset.filter(forms__is_public=True)

        return queryset


class Form(models.Model):
    """
    Represents a works object for a specific works type.
    """

    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
    )

    category = models.ForeignKey(
        FormCategory,
        on_delete=models.CASCADE,
        verbose_name=_("categorie"),
        related_name="forms",
        null=True,
    )
    administrative_entities = models.ManyToManyField(
        AdministrativeEntity,
        verbose_name=_("entités administratives"),
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
    requires_validation_document = models.BooleanField(
        _("Document de validation obligatoire"), default=True
    )
    is_public = models.BooleanField(_("Visibilité "), default=False)
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
    has_geom_intersection_enabled = models.BooleanField(
        _("Activer l'intersection de géométries"), default=False
    )

    # NEW: WorksType
    name = models.CharField(_("nom"), max_length=255)
    order = models.PositiveIntegerField(
        _("ordre"), default=0, blank=False, null=False, db_index=True
    )
    wms_layers = models.URLField(_("Couche(s) WMS"), blank=True, max_length=1024)
    wms_layers_order = models.PositiveIntegerField(
        _("Ordre de(s) couche(s)"), default=1
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

    def clean(self):
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
INPUT_TYPE_TITLE = "title"


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
    INPUT_TYPE_TITLE = INPUT_TYPE_TITLE

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
        (INPUT_TYPE_TITLE, _("Titre")),
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
    )
    name = models.CharField(_("nom"), max_length=255)
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
    file_download = fields.FormFileField(
        _("Fichier"),
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        blank=True,
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
    is_public_when_permitrequest_is_public = models.BooleanField(
        _("Afficher ce champs au grand public si la demande est publique"),
        default=False,
        help_text=_(
            "Ce champs sera visible sur l'application géocalendrier si la demande est publique"
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
