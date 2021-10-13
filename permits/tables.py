import django_tables2 as tables
from django_tables2.utils import A
from django.utils.translation import gettext_lazy as _
from django_tables2_column_shifter.tables import ColumnShiftTable

from . import models


class OwnPermitRequestsTable(ColumnShiftTable):
    actions = tables.TemplateColumn(
        template_name="tables/_permit_request_actions.html",
        verbose_name=_("Actions"),
        orderable=False,
    )
    status = tables.TemplateColumn(template_name="tables/_permit_request_status.html",)
    starts_at_min = tables.Column(verbose_name=_("Début"))
    ends_at_max = tables.Column(verbose_name=_("Fin"))
    prolongation_date = tables.TemplateColumn(verbose_name=_("Prolongation"), template_name="tables/_permit_request_prolongation.html",)
    works_objects_html = tables.Column(
        verbose_name=_("Objets et types de demandes"), orderable=False
    )
    administrative_entity = tables.Column(
        verbose_name=_("Entité administrative"), orderable=False
    )

    class Meta:
        model = models.PermitRequest
        fields = (
            "id",
            "created_at",
            "status",
            "starts_at_min",
            "ends_at_max",
            "prolongation_date",
            "works_objects_html",
            "administrative_entity",
        )
        template_name = "django_tables2/bootstrap.html"


class DepartmentPermitRequestsTable(ColumnShiftTable):
    actions = tables.TemplateColumn(
        template_name="tables/_permit_request_actions.html",
        verbose_name=_("Actions"),
        orderable=False,
    )
    status = tables.TemplateColumn(template_name="tables/_permit_request_status.html",)
    starts_at_min = tables.Column(verbose_name=_("Début"))
    ends_at_max = tables.Column(verbose_name=_("Fin"))
    prolongation_date = tables.TemplateColumn(template_name="tables/_permit_request_prolongation.html",)
    works_objects_html = tables.Column(
        verbose_name=_("Objets et types de demandes"), orderable=False
    )
    administrative_entity = tables.Column(
        verbose_name=_("Entité administrative"), orderable=False
    )
    author_fullname = tables.Column(verbose_name=_("Auteur de la demande"))
    author_details = tables.Column(verbose_name=_("Coordonnées de l'auteur"))

    class Meta:
        model = models.PermitRequest
        fields = (
            "id",
            "author_fullname",
            "author_details",
            "created_at",
            "status",
            "starts_at_min",
            "ends_at_max",
            "prolongation_date",
            "works_objects_html",
            "administrative_entity",
        )
        template_name = "django_tables2/bootstrap.html"

    def before_render(self, request):
        self.columns["actions"].column.extra_context = {
            "can_view": (
                request.user.has_perm("permits.amend_permit_request")
                or request.user.has_perm("permits.validate_permit_request")
                or request.user.has_perm("permits.modify_permit_request")
            )
        }
