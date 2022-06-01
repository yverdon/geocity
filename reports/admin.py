from django.contrib import admin

from .models import Report, ReportLayout


@admin.register(Report)
class ReportLayoutAdmin(admin.ModelAdmin):
    pass


@admin.register(ReportLayout)
class ReportAdmin(admin.ModelAdmin):
    pass
