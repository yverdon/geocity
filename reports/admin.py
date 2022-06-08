from django.contrib import admin

from .models import Report, ReportLayout
from permits.admin import IntegratorFilterMixin


@admin.register(ReportLayout)
class ReportLayoutAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    pass


@admin.register(Report)
class ReportAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "work_object_types":
            if request.user.is_superuser:
                kwargs["queryset"] = Report.objects.all()
            else:
                kwargs["queryset"] = Report.objects.filter(
                    integrator=request.user.groups.get(
                        permitdepartment__is_integrator_admin=True
                    )
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
