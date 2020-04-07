import django_filters
from . import models


class PermitRequestFilterExterns(django_filters.FilterSet):

    class Meta:
        model = models.PermitRequest
        fields = ['status', 'created_at', 'administrative_entity',]
