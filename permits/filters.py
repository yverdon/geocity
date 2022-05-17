import django_filters
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.db.models import Max, Min
from django.utils.translation import gettext_lazy as _

from . import models, services


class BasePermitRequestFilterSet(django_filters.FilterSet):
    id = django_filters.filters.NumberFilter(field_name="id")
    works_object_types__works_type = django_filters.filters.ModelChoiceFilter(
        queryset=models.WorksType.objects.order_by("name"), label=_("Type de demande")
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


def _get_administrative_entities_queryset_for_current_user(request):
    return (
        models.PermitAdministrativeEntity.objects.filter(
            permit_requests__in=services.get_permit_requests_list_for_user(request.user)
        )
        .distinct()
        .order_by("name")
    )


def _get_works_types_queryset_for_current_user(request):
    return (
        models.WorksType.objects.filter(
            works_object_types__permit_requests__in=services.get_permit_requests_list_for_user(
                request.user
            )
        )
        .distinct()
        .order_by("name")
    )


def _get_works_objects_queryset_for_current_user(request):
    return (
        models.WorksObject.objects.filter(
            works_object_types__permit_requests__in=services.get_permit_requests_list_for_user(
                request.user
            )
        )
        .distinct()
        .order_by("name")
    )


class DepartmentPermitRequestFilterSet(BasePermitRequestFilterSet):
    works_object_types__administrative_entities = django_filters.filters.ModelChoiceFilter(
        queryset=_get_administrative_entities_queryset_for_current_user,
        label=_("Entité administrative"),
    )
    works_object_types__works_type = django_filters.filters.ModelChoiceFilter(
        queryset=_get_works_types_queryset_for_current_user, label=_("Type de demande")
    )
    works_object_types__works_object = django_filters.filters.ModelChoiceFilter(
        queryset=_get_works_objects_queryset_for_current_user,
        label=_("Objet de la demande"),
    )
    author__user__last_name = django_filters.filters.CharFilter(
        lookup_expr="icontains", label=_("Auteur de la demande"),
    )

    class Meta:
        model = models.PermitRequest
        fields = [
            "id",
            "status",
            "works_object_types__administrative_entities",
            "works_object_types__works_type",
            "works_object_types__works_object",
            "created_at",
            "starts_at_min",
            "ends_at_max",
            "author__user__last_name",
        ]
