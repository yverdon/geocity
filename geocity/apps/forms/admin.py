import django.db.models
from adminsortable2.admin import SortableAdminMixin
from django import forms
from django.contrib import admin, messages
from django.contrib.admin import AdminSite, site
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group, Permission, User
from django.contrib.sites.admin import SiteAdmin as BaseSiteAdmin
from django.contrib.sites.models import Site
from django.core.management import CommandError, call_command
from django.db.models import Q, Value
from django.db.models.functions import StrIndex, Substr
from django.http import Http404
from django.shortcuts import redirect
from django.urls import re_path, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from geocity.apps.accounts.admin import IntegratorFilterMixin, filter_for_user
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


form_administrative_entities.short_description = _("Entités administratives")


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
        # FIXME rename to form.js
        js = ("js/admin/works_object_type.js",)

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


@admin.register(models.Form)
class FormAdmin(IntegratorFilterMixin, SortableAdminMixin, admin.ModelAdmin):
    form = FormAdminForm
    list_display = [
        "sortable_str",
        form_administrative_entities,
        "can_always_update",
        "is_public",
        "requires_payment",
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
                    "category",
                    "administrative_entities",
                    "can_always_update",
                    "is_public",
                    "requires_payment",
                    "requires_validation_document",
                    "is_anonymous",
                    "integrator",
                )
            },
        ),
        (
            "Notifications aux services",
            {"fields": ("notify_services", "services_to_notify")},
        ),
        (
            "Planning et localisation",
            {
                "fields": (
                    "can_have_multiple_ranges",
                    "geometry_types",
                    "needs_date",
                    "start_delay",
                )
            },
        ),
        (
            "Modules complémentaires",
            {
                "fields": (
                    "document_enabled",
                    "publication_enabled",
                    "permanent_publication_enabled",
                )
            },
        ),
        (
            "Prolongation",
            {
                "fields": (
                    "permit_duration",
                    "expiration_reminder",
                    "days_before_reminder",
                )
            },
        ),
        (
            "Directive",
            {
                "fields": (
                    "directive",
                    "directive_description",
                    "additional_information",
                )
            },
        ),
    )

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = _("1.4 Configuration du type-objet-entité")

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


class FieldForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["forms"] = get_forms_field(user)

    class Meta:
        model = models.Field
        fields = [
            "name",
            "placeholder",
            "help_text",
            "input_type",
            "services_to_notify",
            "choices",
            "line_number_for_textarea",
            "regex_pattern",
            "file_download",
            "is_mandatory",
            "is_public_when_permitrequest_is_public",
            "additional_searchtext_for_address_field",
            "store_geometry_for_address_field",
            "forms",
            "integrator",
        ]

    def clean_file_download(self):
        if self.cleaned_data["input_type"] == "file_download":
            if not self.cleaned_data["file_download"]:
                raise forms.ValidationError(_("This field is required."))
        return self.cleaned_data["file_download"]

    class Media:
        js = ("js/admin/works_object_property.js",)


@admin.register(models.Field)
class FieldAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    form = FieldForm
    list_display = [
        "name",
        "is_mandatory",
        "is_public_when_permitrequest_is_public",
        "input_type",
        "placeholder",
        "help_text",
    ]
    list_filter = [
        "name",
        "input_type",
        "forms",
    ]
    search_fields = [
        "name",
    ]

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
        "id",
    ]

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = _("1.2 Configuration du type")

    def get__tags(self, obj):
        return list(obj.tags.all())

    get__tags.short_description = _("Mots-clés")
