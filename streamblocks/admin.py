from django.contrib import admin
from streamfield.admin import StreamBlocksAdmin

from permits.admin import QgisProjectAdminForm
from .models import PrintBlockMap

admin.site.unregister(PrintBlockMap)
@admin.register(PrintBlockMap)
class PrintBlockMapAdmin(StreamBlocksAdmin, admin.ModelAdmin):
    form = QgisProjectAdminForm
