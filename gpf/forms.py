from django.conf import settings
from django.contrib.gis import forms
from django.forms import widgets
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator
from .models import PermitRequest, Actor, Validation, Document
from .widgets import RemoteAutocompleteWidget
from django.contrib.auth.forms import UserCreationForm
from bootstrap_datepicker_plus import DatePickerInput
import datetime

class SitOpenLayersWidget(forms.OSMWidget):

    template_name = 'openlayers/openlayers.html'
    map_srid = 2056

    @property
    def media(self):
        return forms.Media(
            css={'all': ('libs/js/openlayers/ol.css',)},
            js=('libs/js/openlayers/ol.js',
                'libs/js/proj4js/proj4-src.js',
                'customWidgets/sitMapWidget/sitMapWidget.js'
                ))


class AddPermitRequestForm(forms.ModelForm):

    required_css_class = 'required'

    class Meta:
        model = PermitRequest
        fields = [
            'geom', 'description', 'date_start', 'date_end', 'sitetype', 'address', 'zipcode', 'city',
            'length', 'width', 'road_marking_damaged', 'is_green_area',
            'invoice_to'
        ]
        widgets = {
            'geom': SitOpenLayersWidget(attrs={
                'map_width': '100%',
                'map_height': 500,
                'map_srid': 2056,
                'default_center': [2539057, 1181111],
                'default_zoom': 10,
                'display_raw': False, #show coordinate in debug
                'map_clear_style': "visibility:visible;",
                'edit_geom': True,
                'min_zoom': 8,
                'wmts_capabilities_url': 'https://ows.asitvd.ch/wmts?request=GetCapabilities',
                'wmts_layer': 'asitvd.fond_cadastral',
            }),
            'date_start': DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                    "locale": "fr",
                    "minDate": (datetime.datetime.today() + datetime.timedelta(days=2)).strftime('%Y/%m/%d')
                    }
                ).start_of('event days'),
            'date_end': DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                    "locale": "fr",
                    "minDate": (datetime.datetime.today() + datetime.timedelta(days=2)).strftime('%Y/%m/%d')
                    }
                ).end_of('event days'),
            'description': forms.Textarea(attrs={'rows': '3'}),
            'zipcode': forms.TextInput(attrs={'id': 'id_zipcode_permit'}),
            'city': forms.TextInput(attrs={'id': 'id_city_permit'}),
            'address': RemoteAutocompleteWidget(
                attrs={
                    "id": "id_adress_permit",
                    "apiurl": "https://api3.geo.admin.ch/rest/services/api/SearchServer?",
                    "apiurl_detail": "https://api3.geo.admin.ch/rest/services/api/MapServer/ch.bfs.gebaeude_wohnungs_register/",
                    "search_prefix": "1400 ",
                    "origins": "address",
                    "zipcode_field": "zipcode_permit",
                    "city_field": "city_permit",
                    "placeholder": "ex: Place Pestalozzi 2 Yverdon",
                }),
        }


class ChangePermitRequestForm(forms.ModelForm):

    required_css_class = 'required'

    class Meta:

        model = PermitRequest
        exclude = []
        fields = [
            'company', 'project_owner', 'ended', 'has_existing_archeology', 'has_archeology', 'amount', 'paid', 'validated', 'sent', 'date_start', 'date_end',
            'date_end_work_announcement', 'date_end_work', 'road_marking_damaged', 'date_request_created',
            'is_green_area', 'invoice_to', 'sitetype',
            'description', 'address',  'zipcode', 'city', 'length', 'width', 'geom'
        ]
        help_texts = {
            'validated': "Actif seulement lorsque tous les services ont validé la demande",
            'has_existing_archeology': "Zone archéologique observée au moment de la fouille",
            'has_archeology': "Zone archéologique détectée sur la base des géodonnées cantonales",
            'ended': "La fouille a-t-elle été contrôlée par le bureau STE ?",
        }
        widgets = {
            'geom': SitOpenLayersWidget(attrs={
                'map_width': '100%',
                'map_height': 500,
                'map_srid': 2056,
                'default_center': [2539057, 1181111],
                'default_zoom': 10,
                'display_raw': False, #show coordinate in debug
                'map_clear_style': "visibility:visible;",
                'edit_geom': True,
                'min_zoom': 8,
                'wmts_capabilities_url': 'https://ows.asitvd.ch/wmts?request=GetCapabilities',
                'wmts_layer': 'asitvd.fond_cadastral',
            }),
            'date_start': DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                    "locale": "fr"
                    }
                ).start_of('event days'),
            'date_end': DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                    "locale": "fr"
                    }
                ).end_of('event days'),
            'date_end_work': DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                    "locale": "fr"
                    }
                ),
            'date_end_work_announcement': DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                    "locale": "fr"
                    },
                ),
            'date_request_created': forms.TextInput(
                attrs={'readonly':'readonly'}
            ),
            'description': forms.Textarea(attrs={'rows': '3'}),
            'address': RemoteAutocompleteWidget(
                attrs={
                    "apiurl": "https://api3.geo.admin.ch/rest/services/api/SearchServer?",
                    "apiurl_detail": "https://api3.geo.admin.ch/rest/services/api/MapServer/ch.bfs.gebaeude_wohnungs_register/",
                    "search_prefix": "1400 ",
                    "origins": "address",
                    "zipcode_field": "zipcode",
                    "city_field": "city",
                    "placeholder": "ex: Place Pestalozzi 2 Yverdon",
                }),

        }

class EndWorkForm(forms.ModelForm):
    class Meta:
        model = PermitRequest
        fields = ['date_end_work']
        widgets = {
            'date_end_work': DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                    "locale": "fr"
                    }
                ),
        }


class CompanyForm(forms.ModelForm):

    required_css_class = 'required'

    class Meta:
        model = Actor
        exclude = ['user']
        help_texts = {
            'vat_number': 'Trouvez votre numéro <a href="https://www.bfs.admin.ch/bfs/fr/home/registres/registre-entreprises/numero-identification-entreprises.html" target="_blank">TVA</a>',
        }
        widgets = {
            'address': RemoteAutocompleteWidget(
                attrs={
                    "apiurl": "https://api3.geo.admin.ch/rest/services/api/SearchServer?",
                    "apiurl_detail": "https://api3.geo.admin.ch/rest/services/api/MapServer/ch.bfs.gebaeude_wohnungs_register/",
                    "search_prefix": "",
                    "origins": "address",
                    "zipcode_field": "zipcode",
                    "city_field": "city",
                    "placeholder": "ex: Place Pestalozzi 2 Yverdon",
                }),
            'phone_fixed': forms.TextInput(attrs={'placeholder': 'ex: 024 111 22 22'}),
            'phone_mobile': forms.TextInput(attrs={'placeholder': 'ex: 079 111 22 22'}),
            'vat_number': forms.TextInput(attrs={'placeholder': 'ex: CHE-123.456.789'}),
            'name': forms.TextInput(attrs={'placeholder': 'ex: Dupond'}),
            'firstname': forms.TextInput(attrs={'placeholder': 'ex: Marcel'}),
            'zipcode': forms.TextInput(attrs={'placeholder': 'ex: 1400'}),
            'city': forms.TextInput(attrs={'placeholder': 'ex: Yverdon'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'ex: Construction SA'}),
            'email': forms.TextInput(attrs={'placeholder': 'ex: permis-de-fouille@mapnv.ch'}),
        }


class companyUserAddForm(UserCreationForm):

    required_css_class = 'required'



class ActorForm(forms.ModelForm):

    required_css_class = 'required'

    class Meta:
        model = Actor
        exclude = ['user', 'vat_number']
        widgets = {
            'address': RemoteAutocompleteWidget(
                attrs={
                    "apiurl": "https://api3.geo.admin.ch/rest/services/api/SearchServer?",
                    "apiurl_detail": "https://api3.geo.admin.ch/rest/services/api/MapServer/ch.bfs.gebaeude_wohnungs_register/",
                    "search_prefix": "",
                    "origins": "address",
                    "zipcode_field": "zipcode",
                    "city_field": "city",
                    "placeholder": "ex: Place Pestalozzi 2 Yverdon",
                }),
            'phone_fixed': forms.TextInput(attrs={'placeholder': 'ex: 024 111 22 22'}),
            'phone_mobile': forms.TextInput(attrs={'placeholder': 'ex: 079 111 22 22'}),
            'name': forms.TextInput(attrs={'placeholder': 'ex: Dupond'}),
            'firstname': forms.TextInput(attrs={'placeholder': 'ex: Marcel'}),
            'zipcode': forms.TextInput(attrs={'placeholder': 'ex: 1400'}),
            'city': forms.TextInput(attrs={'placeholder': 'ex: Yverdon'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'ex: Construction SA'}),
            'phone_mobile': forms.TextInput(attrs={'placeholder': 'ex: 079 111 22 22'}),
            'email': forms.TextInput(attrs={'placeholder': 'ex: permis-de-fouille@mapnv.ch'}),
        }


class ValidationForm(forms.ModelForm):
    class Meta:
        model = Validation
        fields = '__all__'
        widgets = {
          'comment': forms.Textarea(attrs={'rows': '3'}),
        }

class DocumentForm(forms.Form):

    file_path = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )

    class Meta:
        model = Document
