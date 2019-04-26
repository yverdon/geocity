from django.db import models
import django_filters
from django_filters.widgets import RangeWidget
from django_filters.filters import DateFromToRangeFilter
from .models import PermitRequest
from bootstrap_datepicker_plus import DatePickerInput
from .widgets import RemoteAutocompleteWidget
from django.contrib.gis import forms


class PermitRequestFilter(django_filters.FilterSet):

    date_end = DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': "dd/mm/yyyy"}))
    date_start = DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': "dd/mm/yyyy"}))


    class Meta:
        model = PermitRequest
        fields = ['id', 'address', 'project_owner', 'company', 'date_end', 'date_start', 'validated', 'paid','ended']
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }


class PermitRequestFilterExterns(django_filters.FilterSet):

    class Meta:
        model = PermitRequest
        fields = ['address', 'validated', 'paid','ended']
