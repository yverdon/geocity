from django.contrib import admin

from .models import BlockAuthor, Report, ReportLayout, BlockMap, BlockParagraph, Block
from permits.admin import IntegratorFilterMixin
from permits import models as permits_models
from django.contrib import admin

from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline


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


class BlockInline(StackedPolymorphicInline):
    model = Block
    # Automatic registration of child inlines
    # see https://django-polymorphic.readthedocs.io/en/stable/admin.html#inline-models
    child_inlines = [
        type(
            f"{child_model.__class__}Inline",
            (StackedPolymorphicInline.Child,),
            {"model": child_model},
        )
        for child_model in Block.__subclasses__()
    ]
    classes = ["grp-module"]


@admin.register(Report)
class ReportAdmin(
    PolymorphicInlineSupportMixin, IntegratorFilterMixin, admin.ModelAdmin
):
    inlines = (BlockInline,)
    filter_horizontal = ("work_object_types",)
    list_display = [
        "name",
        "layout",
        "type",
        "integrator",
    ]
    list_filter = ["name"]
    search_fields = [
        "name",
        "layout",
    ]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "work_object_types":
            if request.user.is_superuser:
                kwargs["queryset"] = permits_models.WorksObjectType.objects.all()
            else:
                kwargs["queryset"] = permits_models.WorksObjectType.objects.filter(
                    integrator=request.user.groups.get(
                        permitdepartment__is_integrator_admin=True
                    )
                )
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        blocks = form.instance.blocks.order_by("order").all()
        for i, block in enumerate(blocks):
            block.order = (i + 1) * 10
            block.save()
