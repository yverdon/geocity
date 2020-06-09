from django.contrib import admin

from . import models


admin.site.register(models.WorksType)
admin.site.register(models.WorksObject)
admin.site.register(models.WorksObjectProperty)
admin.site.register(models.PermitRequest)
admin.site.register(models.PermitActorType)
admin.site.register(models.PermitRequestActor)
admin.site.register(models.PermitActor)
admin.site.register(models.PermitRequestGeoTime)
admin.site.register(models.PermitAuthor)
admin.site.register(models.PermitAdministrativeEntity)
admin.site.register(models.PermitDepartment)
admin.site.register(models.PermitRequestValidation)
admin.site.register(models.WorksObjectPropertyValue)


class WorksObjectTypeAdmin(admin.ModelAdmin):
    list_fields =  ['administrative_entities']


admin.site.register(models.WorksObjectType, WorksObjectTypeAdmin)
