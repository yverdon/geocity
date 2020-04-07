import django_tables2 as tables

from django.utils.translation import gettext_lazy as _

from . import models


class PermitRequestTableExterns(tables.Table):
    edit_properties = tables.TemplateColumn(template_name="tables/_edit_permit_request.html", verbose_name=_('Modifier'), orderable=False)
    submit = tables.TemplateColumn(template_name="tables/_submit_permit_request.html", verbose_name=_('Envoyer'), orderable=False)
    delete = tables.TemplateColumn(template_name="tables/_delete_permit_request.html", verbose_name=_('Supprimer'), orderable=False)

    class Meta:
        model = models.PermitRequest
        fields = ('id', 'status', 'created_at', 'administrative_entity')
        template_name = 'django_tables2/bootstrap.html'


class PermitExportTable(tables.Table):
    class Meta:
        model = models.PermitRequest
        template_name = 'django_tables2/bootstrap.html'
