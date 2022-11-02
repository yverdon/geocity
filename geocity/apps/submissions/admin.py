from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from geocity.apps.accounts.admin import IntegratorFilterMixin, filter_for_user
from geocity.apps.forms.admin import get_forms_field
from geocity.apps.forms.models import Form

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
            "forms",
            "integrator",
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

    def sortable_str(self, obj):
        return str(obj)

    sortable_str.short_description = (
        "2.2 Configuration du champ de traitement des demandes"
    )
    sortable_str.admin_order_field = "name"

    # Pass the user from ModelAdmin to ModelForm
    def get_form(self, request, obj=None, **kwargs):
        Form = super().get_form(request, obj, **kwargs)

        class RequestForm(Form):
            def __new__(cls, *args, **kwargs):
                kwargs["user"] = request.user
                return Form(*args, **kwargs)

        return RequestForm


@admin.register(models.ContactType)
class ContactTypeAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    list_display = [
        "sortable_str",
        "type",
        "form_category",
        "is_mandatory",
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
    sortable_str.short_description = _("1.6 Configuration du contact")

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
    model = models.ComplementaryDocumentType

    def clean(self):
        cleaned_data = super(ComplementaryDocumentTypeAdminForm, self).clean()
        if cleaned_data["parent"] and cleaned_data["form"]:
            raise forms.ValidationError(
                _("Seul les types parents peuvent être lié a un Work Object Type")
            )

        return cleaned_data


@admin.register(models.ComplementaryDocumentType)
class ComplementaryDocumentTypeAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    form = ComplementaryDocumentTypeAdminForm

    fields = ["name", "parent", "form", "integrator"]

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


@admin.register(models.SubmissionInquiry)
class SubmissionInquiryAdmin(admin.ModelAdmin):
    list_display = ("id", "start_date", "end_date", "submitter", "submission")

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = _("3.2 Enquêtes public")
