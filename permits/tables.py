import django_tables2 as tables

from django.utils.translation import gettext_lazy as _

from . import models


class PermitRequestTableExterns(tables.Table):
    actions = tables.TemplateColumn(template_name="tables/_permit_request_actions.html", verbose_name=_('Actions'), orderable=False)

    class Meta:
        model = models.PermitRequest
        fields = ('id', 'status', 'created_at', 'administrative_entity')
        template_name = 'django_tables2/bootstrap.html'


class PermitExportTable(tables.Table):
    class Meta:
        model = models.PermitRequest
        template_name = 'django_tables2/bootstrap.html'
