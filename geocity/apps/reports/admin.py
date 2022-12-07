from django import forms
from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline

from geocity.apps.accounts.admin import IntegratorFilterMixin
from geocity.apps.submissions.models import ComplementaryDocumentType

from .models import Report, ReportLayout, Section


@admin.register(ReportLayout)
class ReportLayoutAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    list_display = [
        "name",
        "font",
        "background",
        "integrator",
    ]
    list_filter = ["name"]
    search_fields = [
        "name",
    ]


# Make sure the inline is always considered changed, even when no input is entered
# (fixes issue where inlines are not saved unless position is defined)
class AlwaysChangedStackedPolymorphicInlineChild(StackedPolymorphicInline.Child):
    # see https://stackoverflow.com/a/3734700
    class AlwaysChangedModelForm(forms.ModelForm):
        def has_changed(self):
            return True

    form = AlwaysChangedModelForm


class SectionInline(StackedPolymorphicInline):
    model = Section
    # Automatic registration of child inlines
    # see https://django-polymorphic.readthedocs.io/en/stable/admin.html#inline-models
    child_inlines = [
        type(
            f"{child_model.__class__}Inline",
            (AlwaysChangedStackedPolymorphicInlineChild,),
            {"model": child_model},
        )
        for child_model in Section.__subclasses__()
    ]

    class Media:
        css = {"all": ("css/admin/reports_admin.css",)}

    classes = ["polymorphic-jazzmin"]


@admin.register(Report)
class ReportAdmin(
    PolymorphicInlineSupportMixin, IntegratorFilterMixin, admin.ModelAdmin
):
    inlines = (SectionInline,)
    filter_horizontal = ("document_types",)
    list_display = [
        "name",
        "layout",
        "integrator",
        "form_",
        "category_",
        "types_",
    ]
    list_filter = [
        "name",
        "layout",
        "integrator",
    ]
    search_fields = [
        "name",
        "layout",
        "integrator",
    ]

    # List forms using the report in admin list
    def form_(self, obj):
        list_content = format_html_join(
            "",
            "<li>{}</li>",
            [[d.parent.form] for d in obj.document_types.all()],
        )
        return mark_safe(f"<ul>{list_content}</ul>")

    # List category (parent) using the report in admin list
    def category_(self, obj):
        list_content = format_html_join(
            "",
            "<li>{}</li>",
            [[d.parent.name] for d in obj.document_types.all()],
        )
        return mark_safe(f"<ul>{list_content}</ul>")

    # List types using the report in admin list
    def types_(self, obj):
        list_content = format_html_join(
            "",
            "<li>{}</li>",
            [[d.name] for d in obj.document_types.all()],
        )
        return mark_safe(f"<ul>{list_content}</ul>")

    form_.short_description = _("Formulaire")
    category_.short_description = _("Catégorie de document")
    types_.short_description = _("Type de document")

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "document_types":
            qs = ComplementaryDocumentType.objects.filter(parent__isnull=False)
            if request.user.is_superuser:
                kwargs["queryset"] = qs.all()
            else:
                kwargs["queryset"] = qs.filter(
                    parent__integrator=request.user.groups.get(
                        permit_department__is_integrator_admin=True
                    )
                )
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        sections = form.instance.sections.order_by("order").all()
        for i, section in enumerate(sections):
            section.order = (i + 1) * 10
            section.save()
