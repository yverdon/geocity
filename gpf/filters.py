from django.db import models
import django_filters
from django_filters.widgets import RangeWidget
from django_filters.filters import DateFromToRangeFilter, DateFilter
from .models import PermitRequest
from bootstrap_datepicker_plus import DatePickerInput
from .widgets import RemoteAutocompleteWidget
from django.contrib.gis import forms


class PermitRequestFilter(django_filters.FilterSet):

    date_end_from = DateFilter(
        field_name = 'date_end',
        lookup_expr = 'gte',
        label = 'Date de fin après le',
        widget =  DatePickerInput(
            options={
                "format": "DD/MM/YYYY",
                "locale": "fr"
                }
            )
    )

    date_end_to = DateFilter(
        field_name = 'date_end',
        lookup_expr = 'lte',
        label = 'Date de fin avant le',
        widget =  DatePickerInput(
            options={
                "format": "DD/MM/YYYY",
                "locale": "fr"
                }
            )
    )

    date_start_from = DateFilter(
        field_name = 'date_start',
        lookup_expr = 'gte',
        label = 'Date de début après le',
        widget =  DatePickerInput(
            options={
                "format": "DD/MM/YYYY",
                "locale": "fr"
                }
            )
    )

    date_start_to = DateFilter(
        field_name = 'date_start',
        lookup_expr = 'lte',
        label = 'Date de début avant le',
        widget =  DatePickerInput(
            options={
                "format": "DD/MM/YYYY",
                "locale": "fr",
                }

            )

    )


    class Meta:
        model = PermitRequest
        fields = {
            'id':  ['exact'],
            'address': ['icontains'],
            'project_owner': ['exact'],
            'company': ['exact'],
            'date_end_from': ['gte'],
            'date_end_to': ['gte'],
            'date_start_from': ['gte'],
            'date_start_to': ['gte'],
            'validated': ['exact'],
            'paid': ['exact'],
            'ended': ['exact']
        }



class PermitRequestFilterExterns(django_filters.FilterSet):

    class Meta:
        model = PermitRequest
        fields = ['address', 'validated', 'paid','ended']
