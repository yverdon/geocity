import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from . import models


class OwnPermitRequestsTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="tables/_permit_request_actions.html",
        verbose_name=_('Actions'),
        orderable=False
    )
    starts_at_min = tables.Column(verbose_name=_("Début"))
    ends_at_max = tables.Column(verbose_name=_("Fin"))
    works_objects_html = tables.Column(
        verbose_name=_("Objets et types de travaux"),
        orderable=False
    )

    class Meta:
        model = models.PermitRequest
        fields = (
            'id',
            'created_at',
            'status',
            'starts_at_min',
            'ends_at_max',
            'administrative_entity',
            'works_objects_html'
        )
        template_name = 'django_tables2/bootstrap.html'


class DepartmentPermitRequestsTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="tables/_permit_request_actions.html",
        verbose_name=_('Actions'),
        orderable=False
    )
    starts_at_min = tables.Column(verbose_name=_("Début"))
    ends_at_max = tables.Column(verbose_name=_("Fin"))
    works_objects_html = tables.Column(
        verbose_name=_("Objets et types de travaux"),
        orderable=False
    )
    administrative_entity = tables.Column(verbose_name=_("Entité administrative"),
                                          orderable=False
                                          )
    author__user__last_name = tables.Column(verbose_name=_("Auteur de la demande"))

    class Meta:
        model = models.PermitRequest
        fields = (
            'id',
            'author__user__last_name',
            'created_at',
            'status',
            'starts_at_min',
            'ends_at_max',
            'works_objects_html',
            'administrative_entity'
        )
        template_name = 'django_tables2/bootstrap.html'

    def before_render(self, request):
        self.columns["actions"].column.extra_context = {
            "can_view": (
                request.user.has_perm("permits.amend_permit_request")
                or request.user.has_perm("permits.validate_permit_request")
                or request.user.has_perm("permits.modify_permit_request")
            )
        }
