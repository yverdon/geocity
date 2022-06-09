from django.contrib import admin

from .models import Report, ReportLayout
from permits.admin import IntegratorFilterMixin
from permits import models as permits_models


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


@admin.register(Report)
class ReportAdmin(IntegratorFilterMixin, admin.ModelAdmin):

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
