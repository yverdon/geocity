from django.db import models
import django_filters
from django_filters.widgets import RangeWidget
from django_filters.filters import DateFilter, CharFilter
from .models import PermitRequest
from bootstrap_datepicker_plus import DatePickerInput
# from .widgets import RemoteAutocompleteWidget
from django.contrib.gis import forms
from django.forms.widgets import TextInput


# class PermitRequestFilter(django_filters.FilterSet):
#
#     date_end_from = DateFilter(
#         field_name = 'date_end',
#         lookup_expr = 'gte',
#         label = 'Date de fin après le',
#         widget =  DatePickerInput(
#             attrs={
#                 "placeholder": "ex: 15/02/2019"
#             },
#             options={
#                 "format": "DD/MM/YYYY",
#                 "locale": "fr"
#                 }
#             )
#     )
#
#     date_end_to = DateFilter(
#         field_name = 'date_end',
#         lookup_expr = 'lte',
#         label = 'Date de fin avant le',
#         widget =  DatePickerInput(
#             attrs={
#                 "placeholder": "ex: 15/02/2019"
#             },
#             options={
#                 "format": "DD/MM/YYYY",
#                 "locale": "fr"
#                 }
#             )
#     )
#
#     date_start_from = DateFilter(
#         field_name = 'date_start',
#         lookup_expr = 'gte',
#         label = 'Date de début après le',
#         widget =  DatePickerInput(
#             attrs={
#                 "placeholder": "ex: 15/02/2019"
#             },
#             options={
#                 "format": "DD/MM/YYYY",
#                 "locale": "fr"
#                 }
#             )
#     )
#
#     date_start_to = DateFilter(
#         field_name = 'date_start',
#         lookup_expr = 'lte',
#         label = 'Date de début avant le',
#         widget =  DatePickerInput(
#             attrs={
#                 "placeholder": "ex: 15/02/2019"
#             },
#             options={
#                 "format": "DD/MM/YYYY",
#                 "locale": "fr",
#                 }
#
#             )
#     )
#
#     address = CharFilter (
#         field_name = 'address',
#         lookup_expr = 'icontains',
#         label = 'L\'adresse contient le texte',
#         widget =  TextInput(
#             attrs={
#                 "placeholder": "ex: pesta"
#             }
#         )
#     )
#
#     company_name = CharFilter (
#         field_name = 'company__company_name',
#         lookup_expr = 'icontains',
#         label = 'La raison sociale contient le texte',
#         widget =  TextInput(
#             attrs={
#                 "placeholder": "ex: taupe"
#             }
#         )
#     )
#
#     project_owner_name = CharFilter (
#         field_name = 'project_owner__name',
#         lookup_expr = 'icontains',
#         label = 'Le nom du maître d\'ouvrage contient le texte',
#         widget =  TextInput(
#             attrs={
#                 "placeholder": "ex: Dupon"
#             }
#         )
#     )
#
#
#
#     class Meta:
#         model = PermitRequest
#         fields = {
#             'id':  ['exact'],
#             'address': ['exact'],
#             'project_owner_name': ['exact'],
#             'company_name': ['exact'],
#             'date_end_from': ['gte'],
#             'date_end_to': ['gte'],
#             'date_start_from': ['gte'],
#             'date_start_to': ['gte'],
#             'validated': ['exact'],
#             'paid': ['exact'],
#             'ended': ['exact']
#         }
#
#         filter_overrides = {
#             models.BooleanField: {
#                 'filter_class': django_filters.BooleanFilter,
#                 'extra': lambda f: {
#                     'widget': forms.CheckboxInput,
#                 },
#             },
#         }



class PermitRequestFilterExterns(django_filters.FilterSet):

    class Meta:
        model = PermitRequest
        fields = ['status', 'created_at', 'administrative_entity',]
