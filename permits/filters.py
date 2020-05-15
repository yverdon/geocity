from django.utils.translation import gettext_lazy as _

import django_filters

from gpf.models import Actor
from . import models, services


class BasePermitRequestFilterSet(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date', label=_("Date de création"))

    class Meta:
        model = models.PermitRequest
        fields = ['status', 'administrative_entity']


class OwnPermitRequestFilterSet(BasePermitRequestFilterSet):
    pass


def permit_request_authors(request):
    return Actor.objects.filter(
        pk__in=services.get_permit_requests_list_for_user(request.user).values_list('author')
    ).order_by('firstname', 'name')


class DepartmentPermitRequestFilterSet(BasePermitRequestFilterSet):
    author = django_filters.filters.ModelChoiceFilter(
        queryset=permit_request_authors
    )
    works_object_types__works_object = django_filters.filters.ModelChoiceFilter(
        queryset=models.WorksObject.objects.order_by('name'),
        label=_("Objet des travaux")
    )
    works_object_types__works_type = django_filters.filters.ModelChoiceFilter(
        queryset=models.WorksType.objects.order_by('name'),
        label=_("Type de travaux")
    )

    class Meta:
        model = models.PermitRequest
        fields = ['status']
