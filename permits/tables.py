from datetime import datetime
import django_tables2 as tables
from django.template.defaultfilters import floatformat
from django.utils.safestring import mark_safe
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


class CustomPropertyValueAccessiblePermitRequest:
    def __init__(self, original_permit_request):
        self.original_permit_request = original_permit_request

    def __getattr__(self, name):
        # In order to retrieve property values, we need to use a custom accessor format
        if name.startswith("#"):
            works_object_filter, property_id = name.strip("#").split("_")
            permit_id = self.original_permit_request.id
            try:
                property_value = models.WorksObjectPropertyValue.objects.get(
                    property__id=property_id,
                    works_object_type_choice__permit_request__id=permit_id,
                    works_object_type_choice__works_object_type__works_object__id=works_object_filter,
                )
                value = property_value.value.get("val", "")
                if (
                    property_value.property.input_type
                    == property_value.property.INPUT_TYPE_CHECKBOX
                ):
                    return _("Oui") if value else _("Non")
                elif (
                    property_value.property.input_type
                    == property_value.property.INPUT_TYPE_NUMBER
                ):
                    return floatformat(value, arg=-2)
                elif (
                    property_value.property.input_type
                    == property_value.property.INPUT_TYPE_LIST_MULTIPLE
                ):
                    return ", ".join(value)
                elif (
                    property_value.property.input_type
                    == property_value.property.INPUT_TYPE_DATE
                    == "date"
                ):
                    return datetime.strptime(value, "%Y-%m-%d").strftime("%d %B %Y")
                else:
                    return value
            except models.WorksObjectPropertyValue.DoesNotExist:
                return None
        return getattr(self.original_permit_request, name)


def get_custom_dynamic_table(inherits_from, extra_column_names):
    # In order to define additional columns at runtime, we need a table class factory
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


class PermitRequestCheckboxColumn(tables.CheckBoxColumn):
    def render(self, value, bound_column, record):
        default = {
            "type": "checkbox",
            "name": "{}[]".format(bound_column.name),
            "value": value,
            "class": "permit-request",
        }
        if self.is_checked(value, record):
            default.update({"checked": "checked"})

        general = self.attrs.get("input")
        specific = self.attrs.get("td__input")
        attrs = tables.utils.AttributeDict(default, **(specific or general or {}))
        return mark_safe("<input %s/>" % attrs.as_html())

    @property
    def header(self):
        """
        In its default implementation, the header property always returns an input
        for the table header, as we do not want this, we override the function to do
        nothing
        """
        return ""


class GenericPermitRequestTable(ColumnShiftTable):
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
    administrative_entity = tables.Column(
        verbose_name=_("Entité administrative"), orderable=False,
    )


class SelectablePermitRequestTable(ColumnShiftTable):
    check = PermitRequestCheckboxColumn(accessor="id", verbose_name="")


class OwnPermitRequestsHTMLTable(
    GenericPermitRequestTable, SelectablePermitRequestTable
):
    works_objects_html = tables.TemplateColumn(
        verbose_name=_("Objets et types de demandes"),
        orderable=False,
        template_name="tables/_permit_request_works_objects.html",
    )
    actions = tables.TemplateColumn(
        template_name="tables/_permit_request_actions.html",
        verbose_name=_("Actions"),
        orderable=False,
    )

    class Meta:
        model = models.PermitRequest
        fields = (
            "check",
            "id",
            "created_at",
            "status",
            "starts_at_min",
            "ends_at_max",
            "works_objects_html",
            "administrative_entity",
        )
        template_name = "django_tables2/bootstrap.html"


class OwnPermitRequestsExportTable(GenericPermitRequestTable):
    works_objects_str = tables.Column(verbose_name=_("Objets et types de demandes"))

    class Meta:
        model = models.PermitRequest
        fields = (
            "id",
            "created_at",
            "status",
            "starts_at_min",
            "ends_at_max",
            "works_objects_str",
            "administrative_entity",
        )
        template_name = "django_tables2/bootstrap.html"


class GenericDepartmentPermitRequestsTable(
    DynamicColumnsTable, GenericPermitRequestTable
):
    administrative_entity = tables.Column(
        verbose_name=_("Entité administrative"), orderable=False,
    )
    author_fullname = tables.Column(
        verbose_name=_("Auteur de la demande"), attrs=ATTRIBUTES, orderable=True,
    )
    author_details = tables.Column(
        verbose_name=_("Coordonnées de l'auteur"), attrs=ATTRIBUTES, orderable=True,
    )

    def before_render(self, request):
        self.columns["actions"].column.extra_context = {
            "can_view": (
                request.user.has_perm("permits.amend_permit_request")
                or request.user.has_perm("permits.validate_permit_request")
                or request.user.has_perm("permits.modify_permit_request")
            )
        }


class DepartmentPermitRequestsHTMLTable(
    GenericDepartmentPermitRequestsTable, SelectablePermitRequestTable
):
    works_objects_html = tables.TemplateColumn(
        verbose_name=_("Objets et types de demandes"),
        orderable=False,
        template_name="tables/_permit_request_works_objects.html",
    )
    actions = tables.TemplateColumn(
        template_name="tables/_permit_request_actions.html",
        verbose_name=_("Actions"),
        orderable=False,
    )

    class Meta:
        model = models.PermitRequest
        fields = (
            "check",
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


class DepartmentPermitRequestsExportTable(GenericDepartmentPermitRequestsTable):
    works_objects_str = tables.Column(verbose_name=_("Objets et types de demandes"))

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
            "works_objects_str",
            "administrative_entity",
        )


class ArchivedPermitRequestsTable(ColumnShiftTable):
    check = PermitRequestCheckboxColumn(accessor="permit_request_id", verbose_name="")
    permit_request_id = tables.Column(verbose_name=_("ID"), orderable=True)
    archived_date = tables.Column(verbose_name=_("Date d'archivage"), orderable=True)
    archivist = tables.Column(verbose_name=_("Archivé par"), orderable=True)
    actions = tables.TemplateColumn(
        template_name="tables/_archived_request_actions.html",
        verbose_name=_("Actions"),
        orderable=False,
    )

    class Meta:
        model = models.ArchivedPermitRequest
        fields = (
            "check",
            "permit_request_id",
            "archived_date",
            "archivist",
        )
        template_name = "django_tables2/bootstrap.html"
