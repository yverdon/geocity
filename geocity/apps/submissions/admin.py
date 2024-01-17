from django import forms
from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from geocity.apps.accounts.admin import IntegratorFilterMixin, filter_for_user
from geocity.apps.accounts.users import get_departments
from geocity.apps.forms.admin import get_forms_field
from geocity.apps.forms.models import Form
from geocity.apps.submissions.payments.models import ServicesFeesType

from . import models


class SubmissionAmendFieldForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["forms"] = get_forms_field(user)

    class Meta:
        model = models.SubmissionAmendField
        fields = [
            "name",
            "is_mandatory",
            "is_visible_by_author",
            "is_visible_by_validators",
            "can_always_update",
            "placeholder",
            "help_text",
            "regex_pattern",
            "forms",
            "integrator",
            "api_name",
            "api_light",
        ]


@admin.register(models.SubmissionAmendField)
class SubmissionAmendFieldAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    list_display = [
        "sortable_str",
        "is_mandatory",
        "is_visible_by_author",
        "is_visible_by_validators",
        "can_always_update",
    ]
    search_fields = [
        "name",
    ]
    form = SubmissionAmendFieldForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "is_mandatory",
                    "is_visible_by_author",
                    "is_visible_by_validators",
                    "can_always_update",
                    "placeholder",
                    "help_text",
                    "regex_pattern",
                    "forms",
                    "integrator",
                )
            },
        ),
        (
            _("API"),
            {
                "fields": (
                    "api_name",
                    "api_light",
                ),
            },
        ),
    )

    def sortable_str(self, obj):
        return str(obj)

    sortable_str.short_description = "Champ de traitement des demandes"
    sortable_str.admin_order_field = "name"

    # Pass the user from ModelAdmin to ModelForm
    def get_form(self, request, obj=None, **kwargs):
        Form = super().get_form(request, obj, **kwargs)

        class RequestForm(Form):
            def __new__(cls, *args, **kwargs):
                kwargs["user"] = request.user
                return Form(*args, **kwargs)

        return RequestForm


@admin.register(models.ContactTypeForAdminSite)
class ContactTypeAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    list_display = [
        "name",
    ]
    search_fields = [
        "name",
    ]

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = _("Types")


@admin.register(models.ContactFormForAdminSite)
class ContactFormAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    list_display = [
        "sortable_str",
        "type",
        "form_category",
        "is_mandatory",
        "is_dynamic",
    ]
    list_filter = [
        "form_category",
        "is_mandatory",
    ]
    search_fields = [
        "name",
    ]

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "type"
    sortable_str.short_description = _("Contact")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "form_category":
            kwargs["queryset"] = filter_for_user(
                request.user, models.FormCategory.objects.all()
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "created_at",
        "sent_date",
        "status",
        "author",
        "get_forms",
        "administrative_entity",
    ]
    search_fields = [
        "id",
        "author__first_name",
        "author__last_name",
    ]
    list_filter = ("status", "author", "forms", "administrative_entity")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related("forms")
            .select_related("author")
        )

    def has_add_permission(self, request):
        return False

    def get_forms(self, obj):
        return ", ".join(sorted([form.name for form in obj.forms.all()]))

    get_forms.admin_order_field = "forms"
    get_forms.short_description = "Formulaires"


class ComplementaryDocumentTypeAdminForm(forms.ModelForm):
    model = models.ComplementaryDocumentTypeForAdminSite

    def clean_form(self):
        form = self.cleaned_data["form"]
        if not self.instance.pk:
            return form
        payment_settings_confirmation_reports = self.instance.children.exclude(
            reports__confirmation_payment_settings_objects=None
        )
        payment_settings_refund_reports = self.instance.children.exclude(
            reports__refund_payment_settings_objects=None
        )
        error_msg = ""
        if (
            payment_settings_confirmation_reports.exists()
            and not payment_settings_confirmation_reports.filter(
                reports__confirmation_payment_settings_objects__form__in=[form]
            )
        ):
            error_msg = _(
                "Ce type de document est utilisé comme confirmation de paiement dans une configuration de paiement, via un modèle d'impression. Vous devez dé-lier le modèle d'impression de la configuration de paiement afin de pouvoir modifier ce champ."
            )
        if (
            payment_settings_refund_reports.exists()
            and not payment_settings_refund_reports.filter(
                reports__refund_payment_settings_objects__form__in=[form]
            )
        ):
            error_msg = _(
                "Ce type de document est utilisé comme remboursement dans une configuration de paiement, via un modèle d'impression. Vous devez dé-lier le modèle d'impression de la configuration de paiement afin de pouvoir modifier ce champ."
            )
        if error_msg:
            raise forms.ValidationError(error_msg)
        return form


class ComplementaryDocumentTypeInline(admin.TabularInline):
    model = models.ComplementaryDocumentTypeForAdminSite
    form = ComplementaryDocumentTypeAdminForm

    fields = ["name"]

    verbose_name = _("Type de document")
    verbose_name_plural = _("Type de documents")

    # Defines the number of extra forms to by default. Default is set to 3
    # https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.InlineModelAdmin.extra
    extra = 1

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(parent__isnull=False)


@admin.register(models.ComplementaryDocumentTypeForAdminSite)
class ComplementaryDocumentTypeAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    inlines = [
        ComplementaryDocumentTypeInline,
    ]
    form = ComplementaryDocumentTypeAdminForm
    fields = ["name", "form", "integrator"]

    def get_list_display(self, request):
        if request.user.is_superuser:
            list_display = [
                "name",
                "form",
                "integrator",
                "types_",
            ]
        else:
            list_display = [
                "name",
                "form",
                "types_",
            ]
        return list_display

    # Fields used in search_fields and list_filter
    integrator_fields = [
        "name",
        "form",
        "integrator",
        "form__administrative_entities",
    ]
    user_fields = [
        "name",
        "form",
    ]

    def get_search_fields(self, request):
        if request.user.is_superuser:
            search_fields = self.integrator_fields
        else:
            search_fields = self.user_fields
        return search_fields

    def get_list_filter(self, request):
        if request.user.is_superuser:
            list_filter = self.integrator_fields
        else:
            list_filter = self.user_fields
        return list_filter

    # List types of documents
    def types_(self, obj):
        list_content = format_html_join(
            "",
            "<li>{}</li>",
            [
                [d]
                for d in models.ComplementaryDocumentType.children_objects.associated_to_parent(
                    obj
                ).values_list(
                    "name", flat=True
                )
            ],
        )
        return mark_safe(f"<ul>{list_content}</ul>")

    types_.short_description = _("Type de document")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "form":
            if request.user.is_superuser:
                kwargs["queryset"] = Form.objects.all()
            else:
                kwargs["queryset"] = Form.objects.filter(
                    integrator=request.user.groups.get(
                        permit_department__is_integrator_admin=True
                    )
                )
        if db_field.name == "parent":
            if request.user.is_superuser:
                kwargs["queryset"] = models.ComplementaryDocumentType.objects.all()
            else:
                kwargs["queryset"] = models.ComplementaryDocumentType.objects.filter(
                    integrator=request.user.groups.get(
                        permit_department__is_integrator_admin=True
                    )
                )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(parent__isnull=True)


@admin.register(models.SubmissionInquiry)
class SubmissionInquiryAdmin(admin.ModelAdmin):
    list_display = ("id", "start_date", "end_date", "submitter", "submission")

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = _("2.3 Enquêtes publiques")


class ServicesFeesTypeAdminForm(forms.ModelForm):
    """Form for managing types of services fees in the admin."""

    def __init__(self, *args, **kwargs):
        current_user = self.current_user

        super().__init__(*args, **kwargs)

        integrator_administrative_entities_list = (
            models.AdministrativeEntity.objects.associated_to_user(current_user)
        )
        self.fields[
            "administrative_entity"
        ].queryset = integrator_administrative_entities_list
        self.initial["administrative_entity"] = integrator_administrative_entities_list[
            0
        ]

    class Meta:
        model = ServicesFeesType
        fields = [
            "administrative_entity",
            "name",
            "fix_price",
            "is_visible_by_validator",
            "integrator",
        ]

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data


@admin.register(ServicesFeesType)
class ServicesFeesTypeAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    """Docstring"""

    list_display = [
        "name",
        "fix_price",
        "administrative_entity",
        "is_visible_by_validator",
        "integrator",
    ]
    search_fields = [
        "name",
        "fix_price",
        "administrative_entity",
    ]
    list_filter = [
        "name",
        "fix_price",
        "administrative_entity",
        "is_visible_by_validator",
        "integrator",
    ]

    form = ServicesFeesTypeAdminForm

    def get_form(self, request, *args, **kwargs):
        form = super(ServicesFeesTypeAdmin, self).get_form(request, *args, **kwargs)
        form.current_user = request.user
        form.department = get_departments(request.user)

        return form

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = _("2.4 Types de prestation")
