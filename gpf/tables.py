import django_tables2 as tables

from .models import PermitRequest

class PermitRequestTable(tables.Table):

    id = tables.Column(order_by=('id'))

    edit_entries = tables.TemplateColumn('<a title="Modifier" href="{% url \'gpf:permitdetail\' record.id %}"> \
        <i class="fa fa-edit fa-lg"></i></a>', verbose_name='Modifier', orderable=False)

    print = tables.TemplateColumn('<a title="Imprimer" onclick="waitMessage()" href="{% url \'gpf:printpermit\' record.id %}"> \
        <i class="fa fa-print fa-lg" style="color:blue"></i></a>', verbose_name='Imprimer', orderable=False)

    administrative = tables.TemplateColumn('<a title="Supprimer" href="{% url \'gpf:permitdelete\' record.id %}"> \
        <i class="fa fa-trash fa-lg" style="color:red"></i></a> | <a title="Envoyer la confirmation" href="{% url \'gpf:sendpermit\' record.id %}"> \
        <i class="fa fa-envelope fa-lg" style="color:green"></i></a> | <a title="Re-demander aux services en attente de valider le permis" href="{% url \'gpf:callforvalidations\' record.id %}"> \
        <i class="fa fa-bullhorn fa-lg" style="color:red"></i></a> | <a title="Voir les personnes n\'ayant pas validé la demande" href="{% url \'gpf:seewaitingvalidations\' record.id %}"> \
        <i class="fa fa-users fa-lg" style="color:blue"></i></a>', verbose_name='Secrétariat', orderable=False, attrs={"td": {"width": "150px"}})

    def before_render(self, request):
        if request.user.has_perm('gpf.change_sent'):
            self.columns.show('administrative')
        else:
            self.columns.hide('administrative')

    class Meta:
        model = PermitRequest
        fields = ('id', 'address', 'date_start', 'date_end', 'date_effective_end', 'paid', 'validated',
        'has_archeology', 'has_existing_archeology', 'sent')
        template_name = 'django_tables2/bootstrap.html'

class PermitRequestTableExterns(tables.Table):

    edit_entries = tables.TemplateColumn('<a title="Anoncer la fin des travaux" href="{% url \'gpf:endwork\' record.id %}"> \
        <i class="fa fa-bullhorn" style="color:green"></i></a>', verbose_name='Actions', orderable=False)

    class Meta:
        model = PermitRequest
        fields = ('address', 'paid', 'validated', 'has_archeology', 'has_existing_archeology')
        template_name = 'django_tables2/bootstrap.html'

class PermitExportTable(tables.Table):

    class Meta:
        model = PermitRequest
        template_name = 'django_tables2/bootstrap.html'
