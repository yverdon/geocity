from django import forms
from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline

from geocity.apps.submissions.models import ComplementaryDocumentType
from geocity.apps.accounts.admin import IntegratorFilterMixin

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
    classes = ["grp-module"]


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
        "types_",
    ]
    list_filter = ["name"]
    search_fields = [
        "name",
        "layout",
    ]

    def types_(self, obj):
        list_content = format_html_join(
            "",
            "<li>{}</li>",
            [[d.name] for d in obj.document_types.all()],
        )
        return mark_safe(f"<ul>{list_content}</ul>")

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "document_types":
            qs = ComplementaryDocumentType.objects.filter(parent__isnull=False)
            if request.user.is_superuser:
                kwargs["queryset"] = qs.all()
            else:
                kwargs["queryset"] = qs.filter(
                    integrator=request.user.groups.get(
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
