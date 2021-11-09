import django_tables2 as tables
from django_tables2.utils import A
from django.utils.translation import gettext_lazy as _
from django_tables2_column_shifter.tables import ColumnShiftTable

from . import models

ATTRIBUTES = {
    "th": {
        "_ordering": {
            "orderable": "orderable",
            "ascending": "asc",
            "descending": "desc",
        }
    }
}


class OwnPermitRequestsTable(ColumnShiftTable):
    actions = tables.TemplateColumn(
        template_name="tables/_permit_request_actions.html",
        verbose_name=_("Actions"),
        orderable=False,
    )
    status = tables.TemplateColumn(
        template_name="tables/_permit_request_status.html",
        attrs=ATTRIBUTES,
        orderable=True,
    )
    starts_at_min = tables.Column(
        verbose_name=_("Début"), attrs=ATTRIBUTES, orderable=True
    )
    ends_at_max = tables.TemplateColumn(
        verbose_name=_("Fin"),
        template_name="tables/_permit_request_ends_at.html",
        attrs=ATTRIBUTES,
        orderable=True,
    )
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
    status = tables.TemplateColumn(
        template_name="tables/_permit_request_status.html",
        attrs=ATTRIBUTES,
        orderable=True,
    )
    starts_at_min = tables.Column(
        verbose_name=_("Début"), attrs=ATTRIBUTES, orderable=True
    )
    ends_at_max = tables.TemplateColumn(
        verbose_name=_("Fin"),
        template_name="tables/_permit_request_ends_at.html",
        attrs=ATTRIBUTES,
        orderable=True,
    )

    works_objects_html = tables.Column(
        verbose_name=_("Objets et types de demandes"), orderable=False,
    )
    administrative_entity = tables.Column(
        verbose_name=_("Entité administrative"), orderable=False,
    )
    author_fullname = tables.Column(
        verbose_name=_("Auteur de la demande"), attrs=ATTRIBUTES, orderable=True,
    )
    author_details = tables.Column(
        verbose_name=_("Coordonnées de l'auteur"), attrs=ATTRIBUTES, orderable=True,
    )

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
