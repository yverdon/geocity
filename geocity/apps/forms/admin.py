import string

import django.db.models
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from constance import config
from django import forms
from django.contrib import admin
from django.urls import reverse
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
    geo_widget_option = forms.ChoiceField(
        choices=models.Form.GEO_WIDGET_CHOICES,
        widget=forms.Select,
        label=_("Choix de l'interface de saisie cartographique"),
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
            "quick_access_slug": forms.TextInput(),
        }
        help_texts = {
            "wms_layers": "URL pour la ou les couches WMS utiles à la saisie de la demande pour ce type d'objet",
            "wms_layers_order": "Ordre de(s) la(les) couche(s) dans la carte. 1: au-dessus",
        }

    @property
    def media(self):
        return forms.Media(
            css={"all": ("css/main.css",)},
            js=("js/admin/form.js", "js/admin/display.js"),
        )

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

        """Advanced geometry widget supports
            - Only points
            - Only one item (no multiple time & map)
            Thus we hide/show related fields and set values programatically
        """

        if (
            int(self.cleaned_data["geo_widget_option"])
            == models.Form.GEO_WIDGET_ADVANCED
        ):
            self.instance.has_geometry_point = True
            self.instance.has_geometry_line = False
            self.instance.has_geometry_polygon = False

            self.instance.can_have_multiple_ranges = False

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
        "custom_api_name",
        form_administrative_entities,
        "quick_access_slug",
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
        "agenda_visible",
    ]
    list_filter = ["administrative_entities"]
    search_fields = [
        "name",
        "category__name",
        "administrative_entities__name",
        "quick_access_slug",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "api_name",
                    "quick_access_slug",
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
                    "geo_widget_option",
                    "map_widget_configuration",
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
        (
            _("Agenda"),
            {"fields": ("agenda_visible",)},
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
        _("Agenda"),
    )

    def sortable_str(self, obj):
        if str(obj) != "":
            sortable_str = str(obj)[:25] + "..." if len(str(obj)) > 25 else str(obj)
            tooltip_text = str(obj)
        else:
            sortable_str = str(obj.pk)
            tooltip_text = None
        return format_html('<span title="{}">{}</span>', tooltip_text, sortable_str)

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = _("Formulaire")

    def custom_api_name(self, obj):
        custom_api_name = (
            obj.api_name[:25] + "..." if len(obj.api_name) > 25 else obj.api_name
        )
        tooltip_text = obj.api_name
        return format_html('<span title="{}">{}</span>', tooltip_text, custom_api_name)

    custom_api_name.admin_order_field = "api_name"
    custom_api_name.short_description = _("Nom dans l'API")

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

        if db_field.name == "map_widget_configuration":
            kwargs["queryset"] = filter_for_user(
                request.user, models.MapWidgetConfiguration.objects.all()
            )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FormWithAdministrativeEntitiesField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        entities = ", ".join(
            entity.name for entity in obj.administrative_entities.all()
        )
        return f"{obj} ({obj.category}) - {entities}"


class ReadOnlyTextInput(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        return value


class FieldAdminForm(forms.ModelForm):
    form_list = forms.CharField(
        required=False, label="Formulaire(s) avec ce champ", widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")

        if instance:
            self.fields["form_list"].widget = ReadOnlyTextInput()
            self.initial["form_list"] = self.get_form_list()

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
            "public_if_submission_public",
            "additional_searchtext_for_address_field",
            "store_geometry_for_address_field",
            "allowed_file_types",
            "integrator",
            "form_list",
            "api_name",
            "api_light",
            "filter_for_api",
        ]

    def get_form_list(self):
        forms_fields = self.instance.form_fields.all().order_by(
            "form__name", "form__id"
        )
        if forms_fields:
            list_content = []
            for ff in forms_fields:
                url = reverse(
                    "admin:forms_form_change", kwargs={"object_id": ff.form.id}
                )
                list_content.append(
                    format_html("<li><a href='{}'>{}</a></li>", url, ff.form.name)
                )
            list_html = "\n".join(list_content)
            return f"<ul>{list_html}</ul>"
        else:
            return "—"

    def clean_file_download(self):
        if self.cleaned_data["input_type"] == "file_download":
            if not self.cleaned_data["file_download"]:
                raise forms.ValidationError(_("This field is required."))
        return self.cleaned_data["file_download"]

    def clean_allowed_file_types(self):
        if (
            self.cleaned_data["input_type"] == "file"
            and self.cleaned_data["allowed_file_types"]
        ):
            global_allowed_file_extensions_list = (
                config.ALLOWED_FILE_EXTENSIONS.translate(
                    str.maketrans("", "", string.whitespace)
                )
                .lower()
                .split(",")
            )

            field_allowed_file_extensions_list = (
                self.cleaned_data["allowed_file_types"]
                .translate(str.maketrans("", "", string.whitespace))
                .lower()
                .split(",")
            )

            extensions_intersect = list(
                set(global_allowed_file_extensions_list).intersection(
                    set(field_allowed_file_extensions_list)
                )
            )

            if len(extensions_intersect) == 0:
                raise forms.ValidationError(
                    _(
                        "Ces extensions ne sont pas autorisées au niveau global de l'application. Les extentensions actuellement autorisées sont: "
                    )
                    + config.ALLOWED_FILE_EXTENSIONS
                )

        return self.cleaned_data["allowed_file_types"]

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
        "custom_api_name",
        "is_mandatory",
        "public_if_submission_public",
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
    fieldsets = (
        (
            None,
            {
                "fields": (
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
                    "additional_searchtext_for_address_field",
                    "store_geometry_for_address_field",
                    "allowed_file_types",
                    "integrator",
                    "form_list",
                )
            },
        ),
        (
            _("API"),
            {
                "fields": (
                    "api_name",
                    "api_light",
                    "filter_for_api",
                    "public_if_submission_public",
                ),
            },
        ),
    )

    def sortable_str(self, obj):
        sortable_str = (
            obj.__str__()[:25] + "..." if len(obj.__str__()) > 25 else obj.__str__()
        )
        tooltip_text = obj.__str__()
        return format_html('<span title="{}">{}</span>', tooltip_text, sortable_str)

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = _("Champ")

    def custom_api_name(self, obj):
        custom_api_name = (
            obj.api_name[:25] + "..." if len(obj.api_name) > 25 else obj.api_name
        )
        tooltip_text = obj.api_name
        return format_html('<span title="{}">{}</span>', tooltip_text, custom_api_name)

    custom_api_name.admin_order_field = "api_name"
    custom_api_name.short_description = _("Nom dans l'API")

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


@admin.register(models.MapWidgetConfiguration)
class FormMapWidgetConfigurationAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    list_display = [
        "name",
        "id",
        "integrator",
    ]

    class Media:
        css = {"all": ("css/admin/map_widget_configurator.css",)}
        js = ("js/admin/map_widget_configurator.js",)
