from datetime import datetime

import django_tables2 as tables
from django.conf import settings
from django.template.defaultfilters import floatformat
from django.utils.safestring import mark_safe
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


class CustomFieldValueAccessibleSubmission:
    def __init__(self, original_submission):
        self.original_submission = original_submission

    def __getattr__(self, name):
        # In order to retrieve property values, we need to use a custom accessor format
        if name.startswith("#"):
            form_filter, field_id = name.strip("#").split("_")
            submission_id = self.original_submission.id
            try:
                field_value = models.FieldValue.objects.get(
                    field_id=field_id,
                    selected_form__submission_id=submission_id,
                    selected_form__form_id=form_filter,
                )
                value = field_value.value.get("val", "")
                if (
                    field_value.field.input_type
                    == field_value.field.INPUT_TYPE_CHECKBOX
                ):
                    return _("Oui") if value else _("Non")
                elif (
                    field_value.field.input_type == field_value.field.INPUT_TYPE_NUMBER
                ):
                    return floatformat(value, arg=-2)
                elif (
                    field_value.field.input_type
                    == field_value.field.INPUT_TYPE_LIST_MULTIPLE
                ):
                    return ", ".join(value)
                elif (
                    field_value.field.input_type
                    == field_value.field.INPUT_TYPE_DATE
                    == "date"
                ):
                    return datetime.strptime(value, "%Y-%m-%d").strftime("%d.%m.%Y")
                else:
                    return value
            except models.FieldValue.DoesNotExist:
                return None
        return getattr(self.original_submission, name)


def get_custom_dynamic_table(inherits_from, extra_column_names):
    # In order to define additional columns at runtime, we need a table class factory
    class custom_class(inherits_from):
        class Meta(inherits_from.Meta):
            fields = tuple(inherits_from.Meta.fields) + extra_column_names

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


class SubmissionCheckboxColumn(tables.CheckBoxColumn):
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


class GenericSubmissionTable(ColumnShiftTable):
    created_at = tables.Column(
        verbose_name=_("Date de création"),
        attrs=ATTRIBUTES,
        orderable=True,
    )
    status = tables.TemplateColumn(
        verbose_name=_("État"),
        # FIXME rename file
        template_name="tables/_submission_status.html",
        attrs=ATTRIBUTES,
        orderable=True,
    )
    starts_at_min = tables.Column(
        verbose_name=_("Début"),
        attrs=ATTRIBUTES,
        orderable=True,
    )
    ends_at_max = tables.TemplateColumn(
        verbose_name=_("Fin"),
        # FIXME rename file
        template_name="tables/_submission_ends_at.html",
        attrs=ATTRIBUTES,
        orderable=True,
    )
    administrative_entity = tables.Column(
        verbose_name=_("Entité administrative"),
        orderable=False,
    )

    def value_starts_at_min(self, record, value):
        return datetime.strftime(value, "%d.%m.%Y %H:%M") if value else ""

    def value_ends_at_max(self, record, value):
        return datetime.strftime(value, "%d.%m.%Y %H:%M") if value else ""

    def value_created_at(self, record, value):
        return datetime.strftime(value, "%d.%m.%Y %H:%M") if value else ""


class SelectableSubmissionTable(ColumnShiftTable):
    check = SubmissionCheckboxColumn(accessor="id", verbose_name="Sélectionner")


class OwnSubmissionsHTMLTable(GenericSubmissionTable, SelectableSubmissionTable):
    forms_html = tables.TemplateColumn(
        verbose_name=_("Objets et types de demandes"),
        orderable=False,
        # FIXME rename template (was _permit_request_works_objects.html)
        template_name="tables/_submission_forms.html",
    )
    actions = tables.TemplateColumn(
        # FIXME rename template
        template_name="tables/_submission_actions.html",
        verbose_name=_("Actions"),
        orderable=False,
    )

    class Meta:
        model = models.Submission
        fields = (
            "check",
            "id",
            "created_at",
            "status",
            "starts_at_min",
            "ends_at_max",
            "forms_html",
            "administrative_entity",
        )
        template_name = "django_tables2/bootstrap.html"


class OwnSubmissionsExportTable(GenericSubmissionTable):
    forms_str = tables.Column(verbose_name=_("Objets et types de demandes"))

    class Meta:
        model = models.Submission
        fields = (
            "id",
            "created_at",
            "status",
            "starts_at_min",
            "ends_at_max",
            "forms_str",
            "administrative_entity",
        )
        template_name = "django_tables2/bootstrap.html"


class GenericDepartmentSubmissionsTable(DynamicColumnsTable, GenericSubmissionTable):
    administrative_entity = tables.Column(
        verbose_name=_("Entité administrative"),
        orderable=False,
    )
    author_fullname = tables.TemplateColumn(
        verbose_name=_("Auteur de la demande"),
        attrs=ATTRIBUTES,
        orderable=True,
        # FIXME probably adapt template contents
        template_name="tables/_submission_author_fullname.html",
    )
    author_details = tables.TemplateColumn(
        verbose_name=_("Coordonnées de l'auteur"),
        attrs=ATTRIBUTES,
        orderable=True,
        # FIXME probably adapt template contents
        template_name="tables/_submission_author_details.html",
    )

    def before_render(self, request):
        self.columns["actions"].column.extra_context = {
            "can_view": (
                request.user.has_perm("submissions.amend_submission")
                or request.user.has_perm("submissions.validate_submission")
                or request.user.has_perm("submissions.modify_submission")
            )
        }


class DepartmentSubmissionsHTMLTable(
    GenericDepartmentSubmissionsTable, SelectableSubmissionTable
):
    forms_html = tables.TemplateColumn(
        verbose_name=_("Objets et types de demandes"),
        orderable=False,
        # FIXME rename template (was _permit_request_works_objects.html)
        template_name="tables/_submission_forms.html",
    )
    actions = tables.TemplateColumn(
        # FIXME rename template
        template_name="tables/_submission_actions.html",
        verbose_name=_("Actions"),
        orderable=False,
    )

    class Meta:
        model = models.Submission
        fields = [
            "check",
            "id",
            "author_fullname",
            "author_details",
            "created_at",
            "status",
            "starts_at_min",
            "ends_at_max",
            "forms_html",
            "administrative_entity",
        ]


class DepartmentSubmissionsExportTable(GenericDepartmentSubmissionsTable):
    forms_str = tables.Column(verbose_name=_("Objets et types de demandes"))

    if settings.AUTHOR_IBAN_VISIBLE:
        author_iban = tables.TemplateColumn(
            verbose_name=_("IBAN"),
            attrs=ATTRIBUTES,
            orderable=False,
            # FIXME rename template
            template_name="tables/_submission_author_iban.html",
        )

    class Meta:
        model = models.Submission
        fields = [
            "id",
            "author_fullname",
            "author_details",
            "created_at",
            "status",
            "starts_at_min",
            "ends_at_max",
            "forms_str",
            "administrative_entity",
        ]

        if settings.AUTHOR_IBAN_VISIBLE:
            fields.insert(3, "author_iban")


class ArchivedSubmissionsTable(ColumnShiftTable):
    check = SubmissionCheckboxColumn(accessor="submission_id", verbose_name="Archiver")
    submission_id = tables.Column(verbose_name=_("ID"), orderable=True)
    archived_date = tables.Column(verbose_name=_("Date d'archivage"), orderable=True)
    archivist = tables.Column(verbose_name=_("Archivé par"), orderable=True)
    actions = tables.TemplateColumn(
        template_name="tables/_archived_submission_actions.html",
        verbose_name=_("Actions"),
        orderable=False,
    )

    class Meta:
        model = models.ArchivedSubmission
        fields = (
            "check",
            "submission_id",
            "archived_date",
            "archivist",
        )
        template_name = "django_tables2/bootstrap.html"
