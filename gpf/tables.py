import django_tables2 as tables
from django.utils.html import format_html

from .models import PermitRequest

class PermitRequestTable(tables.Table):


    edit_entries = tables.TemplateColumn('<a title="Modifier" href="{% url \'gpf:permitdetail\' record.id %}"> \
        <i class="fa fa-edit fa-lg"></i></a>', verbose_name='Modifier', orderable=False)

    print = tables.TemplateColumn('<a title="Imprimer" onclick="waitMessage()" href="{% url \'gpf:printpermit\' record.id %}"> \
        <i class="fa fa-print fa-lg" style="color:#007bff"></i></a>', verbose_name='Imprimer', orderable=False)

    mapnv = tables.TemplateColumn('<a title="Voirs le(s) point(s) dans mapnv.ch" href="{% url \'gpf:mapnv\' record.id %}" target="_blank"> \
        <i class="fa fa-map fa-lg" style="color:#007bff"></i></a>', verbose_name='mapnv', orderable=False)

    administrative = tables.TemplateColumn('<a title="Supprimer" href="{% url \'gpf:permitdelete\' record.id %}"> \
        <i class="fa fa-trash fa-lg" style="color:#007bff"></i></a> | <a title="Envoyer la confirmation" href="{% url \'gpf:sendpermit\' record.id %}"> \
        <i class="fa fa-envelope fa-lg" style="color:#007bff"></i></a> | <a title="Re-demander aux services en attente de valider le permis" href="{% url \'gpf:callforvalidations\' record.id %}"> \
        <i class="fa fa-bullhorn fa-lg" style="color:#007bff"></i></a> | <a title="Voir les personnes n\'ayant pas validé la demande" href="{% url \'gpf:seewaitingvalidations\' record.id %}"> \
        <i class="fa fa-users fa-lg" style="color:#007bff"></i></a>', verbose_name='Secrétariat', orderable=False, attrs={"td": {"width": "150px"}})

    company_link = tables.Column(
        accessor='company',
        verbose_name='Raison sociale',
        linkify=True
    )

    project_owner_link = tables.Column(
        accessor='project_owner',
        verbose_name='Maître d\'ouvrage',
        linkify=True
    )

    id = tables.Column(
        linkify=lambda record: record.get_absolute_url() + '#validations-anchor',
        order_by=('id'),
        verbose_name='Valider',
    )

    def render_company_link(self, value, record):
        return format_html("{}", value.company_name, record.company)

    def before_render(self, request):
        if request.user.has_perm('gpf.change_sent'):
            self.columns.show('administrative')
        else:
            self.columns.hide('administrative')

    class Meta:
        model = PermitRequest
        fields = ('id', 'address', 'company_link', 'project_owner_link', 'date_start', 'date_end', 'paid', 'validated', 'sent', 'mapnv')
        template_name = 'django_tables2/bootstrap.html'


class PermitRequestTableExterns(tables.Table):

    edit_entries = tables.TemplateColumn('<a title="Anoncer la fin des travaux" href="{% url \'gpf:endwork\' record.id %}"> \
        <i class="fa fa-bullhorn" style="color:green"></i></a>', verbose_name='Actions', orderable=False)

    class Meta:
        model = PermitRequest
        fields = ('address', 'paid', 'validated', 'has_archeology', 'archeotype')
        template_name = 'django_tables2/bootstrap.html'

class PermitExportTable(tables.Table):

    class Meta:
        model = PermitRequest
        template_name = 'django_tables2/bootstrap.html'
