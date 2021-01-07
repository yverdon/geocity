import django_filters
from bootstrap_datepicker_plus import DatePickerInput
from django.db.models import Max, Min
from django.utils.translation import gettext_lazy as _

from . import models, services


class BasePermitRequestFilterSet(django_filters.FilterSet):

    works_object_types__works_type = django_filters.filters.ModelChoiceFilter(
        queryset=models.WorksType.objects.order_by("name"), label=_("Type de travaux")
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
        queryset = models.PermitRequest.objects.annotate(
            starts_at_min=Min("geo_time__starts_at"),
            ends_at_max=Max("geo_time__ends_at"),
        )
        fields = [
            "id",
            "status",
            "administrative_entity",
            "works_object_types__works_type",
        ]


class OwnPermitRequestFilterSet(BasePermitRequestFilterSet):
    pass


class DepartmentPermitRequestFilterSet(BasePermitRequestFilterSet):
    author__user__last_name = django_filters.filters.CharFilter(
        lookup_expr='icontains',
        label=_("Auteur de la demande"),
    )
    works_object_types__works_object = django_filters.filters.ModelChoiceFilter(
        queryset=models.WorksObject.objects.order_by("name"),
        label=_("Objet des travaux"),
    )
    works_object_types__works_type = django_filters.filters.ModelChoiceFilter(
        queryset=models.WorksType.objects.order_by("name"), label=_("Type de travaux")
    )

    class Meta:
        model = models.PermitRequest
        fields = ['status']
