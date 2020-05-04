import django_tables2 as tables

from django.utils.translation import gettext_lazy as _

from . import models


class OwnPermitRequestsTable(tables.Table):
    actions = tables.TemplateColumn(template_name="tables/_permit_request_actions.html", verbose_name=_('Actions'), orderable=False)

    class Meta:
        model = models.PermitRequest
        fields = ('id', 'created_at', 'status', 'administrative_entity')
        template_name = 'django_tables2/bootstrap.html'


class SecretariatPermitRequestsTable(tables.Table):
    actions = tables.TemplateColumn(template_name="tables/_permit_request_actions.html", verbose_name=_('Actions'), orderable=False)
    works_objects_html = tables.Column(verbose_name=_("Objets et types de travaux"), orderable=False)

    class Meta:
        model = models.PermitRequest
        fields = ('id', 'created_at', 'status', 'author', 'works_objects_html')
        template_name = 'django_tables2/bootstrap.html'


class PermitExportTable(tables.Table):
    class Meta:
        model = models.PermitRequest
        template_name = 'django_tables2/bootstrap.html'
