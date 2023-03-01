import django_filters
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.db.models import Max, Min
from django.utils.translation import gettext_lazy as _

from geocity.apps.accounts.models import AdministrativeEntity
from geocity.apps.forms.models import Form, FormCategory

from . import models


class BaseSubmissionFilterSet(django_filters.FilterSet):
    id = django_filters.filters.NumberFilter(field_name="id")
    forms__category = django_filters.filters.ModelChoiceFilter(
        queryset=models.FormCategory.objects.order_by("name"),
        label=_("Type de demande"),
    )
    created_at = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date",
        label=_("Date de création le"),
        widget=DatePickerInput(
            attrs={"placeholder": "ex: 15/02/2019"},
            options={"format": "DD/MM/YYYY", "locale": "fr"},
        ),
    )
    starts_at_min = django_filters.DateFilter(
        field_name="starts_at_min",
        lookup_expr="gte",
        label=_("Début après le"),
        widget=DatePickerInput(
            attrs={"placeholder": "ex: 15/02/2019"},
            options={"format": "DD/MM/YYYY", "locale": "fr"},
        ),
    )
    ends_at_max = django_filters.DateFilter(
        field_name="ends_at_max",
        lookup_expr="lte",
        label=_("Fin avant le"),
        widget=DatePickerInput(
            attrs={"placeholder": "ex: 15/02/2019"},
            options={"format": "DD/MM/YYYY", "locale": "fr"},
        ),
    )

    class Meta:
        queryset = models.Submission.objects.annotate(
            starts_at_min=Min("geo_time__starts_at"),
            ends_at_max=Max("geo_time__ends_at"),
        )
        fields = [
            "id",
            "status",
            "administrative_entity",
            "forms__category",
        ]


class OwnSubmissionFilterSet(BaseSubmissionFilterSet):
    pass


def _get_administrative_entities_queryset_for_current_user(request):
    return (
        AdministrativeEntity.objects.filter(
            submissions__in=models.Submission.objects.filter_for_user(request.user)
        )
        .distinct()
        .order_by("name")
    )


def _get_form_categories_queryset_for_current_user(request):
    return (
        FormCategory.objects.filter(
            forms__submissions__in=models.Submission.objects.filter_for_user(
                request.user
            )
        )
        .distinct()
        .order_by("name")
    )


def _get_forms_queryset_for_current_user(request):
    return (
        Form.objects.filter(
            submissions__in=models.Submission.objects.filter_for_user(request.user)
        )
        .distinct()
        .order_by("name")
    )


class DepartmentSubmissionFilterSet(BaseSubmissionFilterSet):
    forms__administrative_entities = django_filters.filters.ModelChoiceFilter(
        queryset=_get_administrative_entities_queryset_for_current_user,
        label=_("Entité administrative"),
    )
    forms__category = django_filters.filters.ModelChoiceFilter(
        queryset=_get_form_categories_queryset_for_current_user,
        label=_("Type de demande"),
    )
    forms = django_filters.filters.ModelChoiceFilter(
        queryset=_get_forms_queryset_for_current_user,
        label=_("Objet de la demande"),
    )
    author__last_name = django_filters.filters.CharFilter(
        lookup_expr="icontains",
        label=_("Auteur de la demande"),
    )
    shortname = django_filters.filters.CharFilter(
        lookup_expr="icontains",
        label=_("Nom court"),
    )

    class Meta:
        model = models.Submission
        fields = [
            "id",
            "shortname",
            "status",
            "forms__administrative_entities",
            "forms__category",
            "forms",
            "created_at",
            "starts_at_min",
            "ends_at_max",
            "author__last_name",
        ]
