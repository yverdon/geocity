import django_tables2 as tables
from django.utils.html import format_html
from .models import PermitRequest


class PermitRequestTableExterns(tables.Table):

    class Meta:
        model = PermitRequest
        fields = ('status', 'created_at', 'administrative_entity')
        template_name = 'django_tables2/bootstrap.html'

class PermitExportTable(tables.Table):

    class Meta:
        model = PermitRequest
        template_name = 'django_tables2/bootstrap.html'
