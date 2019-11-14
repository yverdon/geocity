from django.contrib.gis import admin
from .models import *

admin.site.register(PermitRequest, admin.OSMGeoAdmin)
admin.site.register(Actor)
admin.site.register(Department)
admin.site.register(SiteType)
admin.site.register(Validation)
admin.site.register(Archelogy)
admin.site.register(CreditorType)
admin.site.register(Mail)
admin.site.register(ArcheoType)
admin.site.register(Document)
admin.site.register(AdministrativeEntity)
admin.site.register(ValidationCommentSample)
