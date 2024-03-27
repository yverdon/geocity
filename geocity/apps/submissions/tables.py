import collections
import json
from datetime import datetime, timedelta
from io import BytesIO as IO

import django_tables2 as tables
import pandas
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.db.models import Q
from django.http import FileResponse
from django.template.defaultfilters import floatformat
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django_tables2.export.views import ExportMixin
from django_tables2_column_shifter.tables import ColumnShiftTable

from geocity.apps.accounts.models import AdministrativeEntity

from ..api.serializers import SubmissionPrintSerializer
from . import models
from .payments.models import ServiceFee, Transaction
from .permissions import is_backoffice_of_entity

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
    sent_date = tables.Column(
        verbose_name=_("Date d'envoi"),
        attrs=ATTRIBUTES,
        orderable=True,
    )
    status = tables.TemplateColumn(
        verbose_name=_("État"),
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
        template_name="tables/_submission_ends_at.html",
        attrs=ATTRIBUTES,
        orderable=True,
    )
    administrative_entity = tables.Column(
        verbose_name=_("Entité administrative"),
        orderable=False,
    )
    selected_price = tables.TemplateColumn(
        verbose_name=_("Tarif"),
        template_name="tables/_submission_selected_price.html",
        attrs=ATTRIBUTES,
        orderable=False,
    )

    def value_starts_at_min(self, record, value):
        return datetime.strftime(value, "%d.%m.%Y %H:%M") if value else ""

    def value_ends_at_max(self, record, value):
        return datetime.strftime(value, "%d.%m.%Y %H:%M") if value else ""

    def value_created_at(self, record, value):
        return datetime.strftime(value, "%d.%m.%Y %H:%M") if value else ""

    def value_sent_date(self, record, value):
        return datetime.strftime(value, "%d.%m.%Y %H:%M") if value else ""


class SelectableSubmissionTable(ColumnShiftTable):
    check = SubmissionCheckboxColumn(accessor="id", verbose_name="Sélectionner")


class OwnSubmissionsHTMLTable(DynamicColumnsTable, GenericSubmissionTable):
    forms_html = tables.TemplateColumn(
        verbose_name=_("Objets et types de demandes"),
        orderable=False,
        template_name="tables/_submission_forms.html",
    )
    actions = tables.TemplateColumn(
        template_name="tables/_submission_actions.html",
        verbose_name=_("Actions"),
        orderable=False,
    )

    class Meta:
        model = models.Submission
        fields = (
            "id",
            "created_at",
            "sent_date",
            "status",
            "starts_at_min",
            "ends_at_max",
            "selected_price",
            "forms_html",
            "administrative_entity",
        )
        template_name = "django_tables2/bootstrap.html"


class OwnSubmissionsExportTable(DynamicColumnsTable, GenericSubmissionTable):
    forms_str = tables.TemplateColumn(
        verbose_name=_("Objets et types de demandes"),
        template_name="tables/_submission_forms_str.html",
    )

    class Meta:
        model = models.Submission
        fields = (
            "id",
            "created_at",
            "sent_date",
            "status",
            "starts_at_min",
            "ends_at_max",
            "selected_price",
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
        template_name="tables/_submission_author_fullname.html",
    )
    author_details = tables.TemplateColumn(
        verbose_name=_("Coordonnées de l'auteur"),
        attrs=ATTRIBUTES,
        orderable=True,
        template_name="tables/_submission_author_details.html",
    )

    def before_render(self, request):
        self.columns["actions"].column.extra_context = {
            "can_view": (
                request.user.has_perm("submissions.amend_submission")
                or request.user.has_perm("submissions.validate_submission")
                or request.user.has_perm("submissions.modify_submission")
                or request.user.has_perm("submissions.read_submission")
            )
        }


class DepartmentSubmissionsHTMLTable(
    GenericDepartmentSubmissionsTable, SelectableSubmissionTable
):
    forms_html = tables.TemplateColumn(
        verbose_name=_("Objets et types de demandes"),
        orderable=False,
        template_name="tables/_submission_forms.html",
    )
    actions = tables.TemplateColumn(
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
            "sent_date",
            "status",
            "starts_at_min",
            "ends_at_max",
            "selected_price",
            "forms_html",
            "administrative_entity",
        ]


class DepartmentSubmissionsExportTable(GenericDepartmentSubmissionsTable):
    forms_str = tables.TemplateColumn(
        verbose_name=_("Objets et types de demandes"),
        template_name="tables/_submission_forms_str.html",
    )

    if settings.AUTHOR_IBAN_VISIBLE:
        author_iban = tables.TemplateColumn(
            verbose_name=_("IBAN"),
            template_name="tables/_submission_author_iban.html",
        )

    class Meta:
        model = models.Submission
        fields = [
            "id",
            "author_fullname",
            "author_details",
            "created_at",
            "sent_date",
            "status",
            "starts_at_min",
            "ends_at_max",
            "selected_price",
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


class TransactionsTable(tables.Table):
    creation_date = tables.Column(verbose_name=_("Date de création"), orderable=False)
    updated_date = tables.Column(
        verbose_name=_("Date de modification"), orderable=False
    )
    transaction_type = tables.Column(
        verbose_name=_("Type de transaction"), orderable=False
    )
    transaction_id = tables.Column(verbose_name=_("ID transaction"), orderable=False)
    amount = tables.Column(verbose_name=_("Montant"), orderable=False)
    currency = tables.Column(verbose_name=_("Devise"), orderable=False)
    status = tables.Column(verbose_name=_("Statut"), orderable=False)
    actions = tables.TemplateColumn(
        template_name="tables/_submission_transactions_table_actions.html",
        verbose_name="",
        orderable=False,
    )

    class Meta:
        model = Transaction
        fields = (
            "transaction_id",
            "transaction_type",
            "creation_date",
            "updated_date",
            "amount",
            "currency",
            "status",
        )
        template_name = "django_tables2/bootstrap.html"


class MonetaryAmountColumn(tables.Column):
    total_monetary_amount = 0

    def render(self, value, bound_column, record):
        self.total_monetary_amount += value
        return value

    def render_footer(self, bound_column, table):
        return self.total_monetary_amount


class ServiceFeeTable(tables.Table):
    class MoneteryAmountColumn(tables.Column):
        total_monetary_amount = 0

        def render(self, value, bound_column, record):
            self.total_monetary_amount += value
            return value

        def render_footer(self, bound_column, table):
            return self.total_monetary_amount

    class TimeSpentOnTaskAmountColumn(tables.Column):
        time_spent_on_task_amount = 0

        def render(self, value, bound_column, record):
            self.time_spent_on_task_amount += value.total_seconds()
            return value

        def render_footer(self, bound_column, table):
            return timedelta(seconds=self.time_spent_on_task_amount)

    class ProvidedByFullName(tables.Column):
        def render(self, value, bound_column, record):
            return value.get_full_name()

    permit_department = tables.Column(
        verbose_name=_("Service"),
        orderable=False,
        footer=_("Total CHF"),
    )
    service_fee_type = tables.Column(
        verbose_name=_("Prestation"),
        orderable=False,
    )
    provided_by = ProvidedByFullName(
        verbose_name=_("Saisie par"),
        orderable=False,
    )
    provided_at = tables.Column(
        verbose_name=_("Date de création"),
        orderable=False,
    )
    time_spent_on_task = TimeSpentOnTaskAmountColumn(
        verbose_name=_("Durée [hh:mm:ss]"),
        orderable=False,
    )
    hourly_rate = tables.Column(
        verbose_name=_("Tarif horaire [CHF]"),
        orderable=False,
    )
    monetary_amount = MonetaryAmountColumn(
        verbose_name=_("Montant [CHF]"),
        orderable=False,
    )
    actions = tables.TemplateColumn(
        template_name="tables/_submission_service_fees_table_actions.html",
        verbose_name=_("Actions"),
        orderable=False,
    )

    class Meta:
        model = ServiceFee
        fields = (
            "permit_department",
            "service_fee_type",
            "provided_by",
            "provided_at",
            "time_spent_on_task",
            "hourly_rate",
            "monetary_amount",
        )
        empty_text = _("Le tableau des prestations est actuellement vide.")
        template_name = "django_tables2/bootstrap.html"


class PandasExportMixin(ExportMixin):
    def create_export(self, export_format):
        advanced = self.request.GET.get("_advanced", False)

        if not export_format in ["xlsx"]:
            raise NotImplementedError

        if not advanced:
            return super().create_export(export_format)

        # Retrieve entities associated to the user
        entities = AdministrativeEntity.objects.associated_to_user(self.request.user)

        # Take all submission except status draft
        submissions_qs = self.get_pandas_table_data().filter(
            Q(administrative_entity__in=entities),
            ~Q(status=models.Submission.STATUS_DRAFT),
        )

        # Doesn't export all datas, if there's any submission of an entity where user isn't backoffice
        for submission in submissions_qs:
            if not is_backoffice_of_entity(
                self.request.user, submission.administrative_entity
            ):
                return super().create_export(export_format)

        records = {}

        # Make sure there will be no bypass
        submissions_list = submissions_qs.values_list("id", flat=True)
        visible_submissions_for_user = models.Submission.objects.filter_for_user(
            self.request.user,
        ).values_list("id", flat=True)

        if not all(item in visible_submissions_for_user for item in submissions_list):
            raise SuspiciousOperation

        for submission in submissions_qs:
            list_selected_forms = list(
                submission.selected_forms.values_list("form_id", flat=True)
            )

            # Handle null selected_forms (due to old bug YC-1093)
            if list_selected_forms:
                sheet_name = "_".join(map(str, list_selected_forms))
                ordered_dict = SubmissionPrintSerializer(submission).data
                ordered_dict.move_to_end("geometry")
                data_dict = dict(ordered_dict)
                data_str = json.dumps(data_dict)
                record = json.loads(data_str, object_pairs_hook=collections.OrderedDict)

                if sheet_name not in records.keys():
                    records[sheet_name] = []
                records[sheet_name].append(record)

        now = timezone.now()

        if export_format == "xlsx":
            excel_file = IO()
            excel_writer = pandas.ExcelWriter(excel_file)

            for key in records:
                data_frame = pandas.json_normalize(records[key])
                data_frame.to_excel(excel_writer, sheet_name=key)

            excel_writer.close()
            excel_file.seek(0)
            filename = f"geocity_export_{now:%Y-%m-%d}.xlsx"

            content_type = "content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'"

        response = FileResponse(
            excel_file,
            filename=filename,
            as_attachment=False,
        )
        response["Content-Type"] = content_type
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        return response
