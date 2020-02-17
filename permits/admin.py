from django.contrib import admin

from . import models


admin.site.register(models.WorksType)
admin.site.register(models.WorksObject)
admin.site.register(models.WorksObjectType)
admin.site.register(models.WorksObjectProperty)
admin.site.register(models.PermitRequest)
admin.site.register(models.PermitActorType)
