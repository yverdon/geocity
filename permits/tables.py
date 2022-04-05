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


class CustomAccessablePermitRequest:
    def __init__(self, original_permit_request):
        self.original_permit_request = original_permit_request

    def __getattr__(self, name):
        if name.startswith("#"):
            works_object_filter, property_id = name.strip("#").split("_")
            permit_id = self.original_permit_request.id
            try:
                property_value = models.WorksObjectPropertyValue.objects.get(
                    property__id=property_id,
                    works_object_type_choice__permit_request__id=permit_id,
                    works_object_type_choice__works_object_type__works_object__id=works_object_filter,
                )
                return property_value.value.get("val", "")
            except models.WorksObjectPropertyValue.DoesNotExist:
                return None
        return getattr(self.original_permit_request, name)


def get_custom_dynamic_table(inherits_from, extra_column_names, fields_go_before):
    class custom_class(inherits_from):
        class Meta(inherits_from.Meta):
            fields = inherits_from.Meta.fields + extra_column_names

    return custom_class


class DynamicColumnsTable(ColumnShiftTable):
    def __init__(self, *args, extra_column_specs=[], **kwargs):
        # Clone the original static column specs to restore it later
        bc = type(self.base_columns)(self.base_columns)

        for extra_name, extra_column in extra_column_specs:
            # Here, "self" is the Metaclass, not the Table's instance
            self.base_columns[extra_name] = extra_column

        ColumnShiftTable.__init__(self, *args, **kwargs)
        # Restore original static specs for future uses
        type(self).base_columns = bc


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


class DepartmentPermitRequestsTable(DynamicColumnsTable):

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

    # works_objects_html = tables.Column(
    #     verbose_name=_("Objets et types de demandes"), orderable=False,
    # )
    works_objects_html = tables.TemplateColumn(
        verbose_name=_("Objets et types de demandes"),
        orderable=False,
        template_name="tables/_permit_request_works_objects.html",
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
