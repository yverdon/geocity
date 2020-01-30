import django_tables2 as tables
from django.utils.html import format_html
from .models import PermitRequest


class PermitRequestTableExterns(tables.Table):

    edit_properties = tables.TemplateColumn('<a title="Modifier" href="{% url \'permits:permit_request_properties\' record.id %}"> \
     <i class="fa fa-edit fa-lg permit_status_{{record.status}}"></i></a>', verbose_name='Modifier', orderable=False)

    submit = tables.TemplateColumn('<a title="Modifier" href="{% url \'permits:permit_request_submit\' record.id %}"> \
    <i class="fa fa-envelope fa-lg permit_status_{{record.status}}"></i></a>', verbose_name='Envoyer', orderable=False)

    delete = tables.TemplateColumn('<a title="Supprimer la demande" href="{% url \'permits:permit_request_delete\' record.id %}"> \
    <i class="fa fa-trash fa-lg"></i></a>', verbose_name='Supprimer', orderable=False)


    class Meta:
        model = PermitRequest
        fields = ('id', 'status', 'created_at', 'administrative_entity')
        template_name = 'django_tables2/bootstrap.html'

class PermitExportTable(tables.Table):

    class Meta:
        model = PermitRequest
        template_name = 'django_tables2/bootstrap.html'
