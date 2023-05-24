import django.db.models
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from geocity.apps.accounts.admin import (
    LEGAL_TEXT_EXAMPLE,
    IntegratorFilterMixin,
    filter_for_user,
)
from geocity.apps.accounts.models import PUBLIC_TYPE_CHOICES, AdministrativeEntity

from . import models

PERMIT_DURATION_ERROR_MESSAGE = "Veuillez saisir une valeur > 0"
DAYS_BEFORE_REMINDER_ERROR_MESSAGE = (
    "Si la fonction de rappel est active, il faut saisir une valeur de délai valide"
)


def form_administrative_entities(obj):
    return ", ".join(
        administrative_entity.name
        for administrative_entity in obj.administrative_entities.all()
    )


form_administrative_entities.short_description = _("Entité administrative")


def get_forms_field(user):
    qs = (
        models.Form.objects.select_related("category")
        .order_by("name", "category__name")
        .prefetch_related("administrative_entities")
    )

    if not user.is_superuser:
        qs = qs.filter(
            integrator__in=user.groups.filter(
                permit_department__is_integrator_admin=True
            )
        )

    return FormWithAdministrativeEntitiesField(
        queryset=qs,
        widget=forms.CheckboxSelectMultiple,
        label=_("formulaires").capitalize(),
    )


class FormAdminForm(forms.ModelForm):
    class GeometryTypes(django.db.models.TextChoices):
        POINT = "has_geometry_point", _("Point")
        LINE = "has_geometry_line", _("Ligne")
        POLYGON = "has_geometry_polygon", _("Polygone")

    geometry_types = forms.MultipleChoiceField(
        choices=GeometryTypes.choices,
        widget=forms.CheckboxSelectMultiple,
        label=_("Types de géométrie autorisés"),
        required=False,
    )

    class Meta:
        model = models.Form
        fields = "__all__"
        widgets = {
            "is_public": forms.RadioSelect(
                choices=PUBLIC_TYPE_CHOICES,
            ),
            "wms_layers": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "ex: https://mywmserver.ch?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&"
                    + "FORMAT=image%2Fpng&TRANSPARENT=true&LAYERS=my_layer_name&SERVERTYPE="
                    + "mapserver&CRS=EPSG%3A2056",
                }
            ),
        }
        help_texts = {
            "wms_layers": "URL pour la ou les couches WMS utiles à la saisie de la demande pour ce type d'objet",
            "wms_layers_order": "Ordre de(s) la(les) couche(s) dans la carte. 1: au-dessus",
        }

    class Media:
        js = ("js/admin/form.js",)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        if instance:
            kwargs["initial"] = dict(
                geometry_types=[
                    geometry_type
                    for geometry_type in self.GeometryTypes.values
                    if getattr(instance, geometry_type)
                ],
                **kwargs.get("initial", {}),
            )

        super().__init__(*args, **kwargs)

    # TODO: remove this once M2M relation is removed in model
    def clean_administrative_entities(self):
        administrative_entities = self.cleaned_data["administrative_entities"]
        if len(administrative_entities) > 1:
            raise forms.ValidationError(
                _("Une seule entité administrative peut être sélectionnée")
            )
        return administrative_entities

    def clean_days_before_reminder(self):
        if (
            self.cleaned_data["expiration_reminder"]
            and self.cleaned_data["days_before_reminder"] is None
        ):
            raise forms.ValidationError(DAYS_BEFORE_REMINDER_ERROR_MESSAGE)
        return self.cleaned_data["days_before_reminder"]

    def clean_permit_duration(self):
        if self.cleaned_data["permit_duration"]:
            if self.cleaned_data["permit_duration"] <= 0:
                raise forms.ValidationError(PERMIT_DURATION_ERROR_MESSAGE)
        return self.cleaned_data["permit_duration"]

    def save(self, *args, **kwargs):
        for geometry_type in self.GeometryTypes.values:
            setattr(
                self.instance,
                geometry_type,
                geometry_type in self.cleaned_data["geometry_types"],
            )

        return super().save(*args, **kwargs)


# TODO: enable drag and drop for inline reorder
class FormFieldInline(admin.TabularInline, SortableInlineAdminMixin):
    model = models.FormField
    extra = 2
    verbose_name = _("Champ")
    verbose_name_plural = _("Champs")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Display only the fields that belongs to current integrator user
        if db_field.name == "field":
            kwargs["queryset"] = filter_for_user(
                request.user, models.Field.objects.all()
            )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FormPricesInline(admin.TabularInline, SortableInlineAdminMixin):
    model = models.Form.prices.through
    extra = 1
    verbose_name = _("Tarif")
    verbose_name_plural = _("Tarifs")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Display only the fields that belongs to current integrator user
        if db_field.name == "price":
            kwargs["queryset"] = filter_for_user(
                request.user, models.Price.objects.all()
            )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.Form)
class FormAdmin(SortableAdminMixin, IntegratorFilterMixin, admin.ModelAdmin):
    form = FormAdminForm
    inlines = [
        FormPricesInline,
        FormFieldInline,
    ]
    list_display = [
        "sortable_str",
        form_administrative_entities,
        "can_always_update",
        "is_public",
        "requires_payment",
        "requires_online_payment",
        "payment_settings",
        "requires_validation_document",
        "is_anonymous",
        "notify_services",
        "needs_date",
        "permit_duration",
        "expiration_reminder",
        "days_before_reminder",
        "has_geometry_point",
        "has_geometry_line",
        "has_geometry_polygon",
        "document_enabled",
        "publication_enabled",
        "permanent_publication_enabled",
        "max_submissions_nb_submissions",
        "get_max_submissions_message",
    ]
    list_filter = ["administrative_entities"]
    search_fields = [
        "name",
        "category__name",
        "administrative_entities__name",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "category",
                    "administrative_entities",
                    "can_always_update",
                    "is_public",
                    "requires_validation_document",
                    "max_submissions",
                    "max_submissions_message",
                    "is_anonymous",
                    "integrator",
                )
            },
        ),
        (
            _("Directives - Données personnelles"),
            {
                "fields": (
                    "directive",
                    "directive_description",
                    "additional_information",
                ),
                "description": format_html(
                    f"""<p>Saisir ici les directives et informations obligatoires concernant la protection des données personnelles.
                    Note: si ces informations ont une portée globale pour toute l'entité, cette information peut être saisie à l'étape 1.1 Entité administrative</p>
                     <hr>
                    {LEGAL_TEXT_EXAMPLE}
                    """
                ),
            },
        ),
        (
            _("Planning et localisation"),
            {
                "fields": (
                    "can_have_multiple_ranges",
                    "needs_date",
                    "start_delay",
                    "permit_duration",
                    "expiration_reminder",
                    "days_before_reminder",
                    "geometry_types",
                    "wms_layers",
                    "wms_layers_order",
                )
            },
        ),
        (
            _("Notifications aux services"),
            {"fields": ("notify_services", "services_to_notify")},
        ),
        (
            _("Modules complémentaires"),
            {
                "fields": (
                    "document_enabled",
                    "publication_enabled",
                    "permanent_publication_enabled",
                )
            },
        ),
        (
            _("Paiements"),
            {
                "fields": (
                    "requires_payment",
                    "requires_online_payment",
                    "payment_settings",
                )
            },
        ),
    )
    jazzmin_section_order = (
        None,
        _("Directives - Données personnelles"),
        _("Planning et localisation"),
        _("Notifications aux services"),
        _("Modules complémentaires"),
        _("Champs"),
        _("Paiements"),
        _("Tarifs"),
    )

    def sortable_str(self, obj):
        return str(obj) if str(obj) != "" else str(obj.pk)

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = _("Formulaire")

    def max_submissions_nb_submissions(self, obj):
        nb_submissions_str = _("demandes actuellement")
        return (
            f"{obj.max_submissions} ({obj.nb_submissions_taken_into_account_for_max_submissions} {nb_submissions_str})"
            if obj.max_submissions
            else "-"
        )

    max_submissions_nb_submissions.admin_order_field = "max_submissions"
    max_submissions_nb_submissions.short_description = _("Nombre maximum de demandes")

    def get_max_submissions_message(self, obj):
        return obj.max_submissions_message if obj.max_submissions else "-"

    get_max_submissions_message.admin_order_field = "max_submissions_message"
    get_max_submissions_message.short_description = _(
        "Message lorsque le nombre maximal est atteint"
    )

    def get_queryset(self, request):
        qs = (
            super()
            .get_queryset(request)
            .select_related("category")
            .prefetch_related("administrative_entities")
        )
        return qs

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "administrative_entities":
            if request.user.is_superuser:
                kwargs["queryset"] = AdministrativeEntity.objects.all()
            else:
                kwargs["queryset"] = AdministrativeEntity.objects.filter(
                    integrator=request.user.groups.get(
                        permit_department__is_integrator_admin=True
                    )
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user

        if db_field.name == "category":
            qs = models.FormCategory.objects.all()
            kwargs["queryset"] = filter_for_user(user, qs)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FormWithAdministrativeEntitiesField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        entities = ", ".join(
            entity.name for entity in obj.administrative_entities.all()
        )
        return f"{obj} ({obj.category}) - {entities}"


class FieldAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Field
        fields = [
            "name",
            "placeholder",
            "help_text",
            "input_type",
            "services_to_notify",
            "message_for_notified_services",
            "choices",
            "line_number_for_textarea",
            "regex_pattern",
            "file_download",
            "is_mandatory",
            "is_public_when_permitrequest_is_public",
            "additional_searchtext_for_address_field",
            "store_geometry_for_address_field",
            "integrator",
        ]

    def clean_file_download(self):
        if self.cleaned_data["input_type"] == "file_download":
            if not self.cleaned_data["file_download"]:
                raise forms.ValidationError(_("This field is required."))
        return self.cleaned_data["file_download"]

    class Media:
        js = ("js/admin/form_field.js",)


class PriceAdminForm(forms.ModelForm):
    class Meta:
        model = models.Price
        fields = ["text", "amount", "currency", "integrator"]


class PriceByEntityListFilter(admin.SimpleListFilter):
    title = _("Entité administrative")
    parameter_name = "entity"

    def lookups(self, request, model_admin):
        entities = AdministrativeEntity.objects.filter(
            forms__prices__isnull=False
        ).distinct()
        return ((entity.pk, entity.name) for entity in entities)

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(forms__administrative_entities__id=self.value())

        return queryset


@admin.register(models.Price)
class PriceAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    form = PriceAdminForm
    list_display = ["text", "amount", "currency", "entities", "form_names"]
    list_filter = ["text", "amount", PriceByEntityListFilter]
    readonly_fields = ["currency"]
    search_fields = [
        "name",
    ]

    def entities(self, obj):
        entities = (
            AdministrativeEntity.objects.filter(forms__prices=obj)
            .distinct()
            .values_list("name", flat=True)
        )
        return ", ".join(entities) if entities else "-"

    entities.short_description = _("Entité(s) administrative(s)")

    def form_names(self, obj):
        form_names = (form.name for form in obj.forms.all())
        return ", ".join(form_names) if form_names else "-"

    form_names.short_description = _("Form(s)")


class PaymentSettingsForm(forms.ModelForm):
    class Meta:
        model = models.PaymentSettings
        fields = [
            "name",
            "prices_label",
            "payment_confirmation_report",
            "payment_refund_report",
            "internal_account",
            "payment_processor",
            "space_id",
            "user_id",
            "api_key",
            "integrator",
        ]


@admin.register(models.PaymentSettings)
class PaymentSettingsAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    form = PaymentSettingsForm
    list_display = ["name", "prices_label", "payment_processor"]
    list_filter = ["name", "internal_account", "payment_processor"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["payment_confirmation_report", "payment_refund_report"]:
            kwargs["queryset"] = filter_for_user(
                request.user, models.Report.objects.all()
            )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.Field)
class FieldAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    form = FieldAdminForm
    list_display = [
        "sortable_str",
        "is_mandatory",
        "is_public_when_permitrequest_is_public",
        "input_type",
        "placeholder",
        "help_text",
    ]
    list_filter = [
        "name",
        "input_type",
    ]
    search_fields = [
        "name",
    ]

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = _("Champ")

    # Pass the user from ModelAdmin to ModelForm
    def get_form(self, request, obj=None, **kwargs):
        Form = super().get_form(request, obj, **kwargs)

        class RequestForm(Form):
            def __new__(cls, *args, **kwargs):
                kwargs["user"] = request.user
                return Form(*args, **kwargs)

        return RequestForm


class FormCategoryAdminForm(forms.ModelForm):
    class Meta:
        model = models.FormCategory
        fields = [
            "name",
            "meta_type",
            "tags",
            "integrator",
        ]


@admin.register(models.FormCategory)
class FormCategoryAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    form = FormCategoryAdminForm
    list_display = [
        "sortable_str",
        "meta_type",
        "get__tags",
    ]
    search_fields = [
        "name",
    ]

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = _("Catégorie")

    def get__tags(self, obj):
        return list(obj.tags.all())

    get__tags.short_description = _("Mots-clés")
    get__tags.admin_order_field = "tags__name"
