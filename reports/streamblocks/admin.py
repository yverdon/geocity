from django.contrib import admin
from streamfield.admin import StreamBlocksAdmin

from permits.admin import QgisProjectAdminForm
from . import models


# django-streamfield auto-registers the models, we need to unregister them
# to customize their admin
# see: https://github.com/raagin/django-streamfield#custom-admin-class-for-blocks-models
admin.site.unregister(models.PrintBlockRichText)
admin.site.unregister(models.PrintBlockCustom)
admin.site.unregister(models.PrintBlockMap)
admin.site.unregister(models.PrintBlockContacts)
admin.site.unregister(models.PrintBlockValidation)


@admin.register(models.PrintBlockRichText)
@admin.register(models.PrintBlockCustom)
@admin.register(models.PrintBlockContacts)
@admin.register(models.PrintBlockValidation)
class PrintBlockAdmin(StreamBlocksAdmin):
    # prevent the model from showing up in the index page
    def has_module_permission(self, request):
        return False


@admin.register(models.PrintBlockMap)
class PrintBlockMapAdmin(PrintBlockAdmin):
    # use a form that takes care of processing the QGIS project so that it works internally
    form = QgisProjectAdminForm
