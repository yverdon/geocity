from django.conf import settings
from django.contrib.gis import forms
from django.forms import widgets
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
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
            'administrative_entity', 'address', 'geom', 'description', 'date_start', 'date_end', 'sitetype',
            'length', 'width', 'road_marking_damaged', 'is_green_area',
            'invoice_to'
        ]
        widgets = {
            'geom': SitOpenLayersWidget(attrs={
                'map_width': '100%',
                'map_height': settings.OL_MAP_HEIGHT,
                'map_srid': 2056,
                'default_center': [2539057, 1181111],
                'default_zoom': 10,
                'display_raw': False, #show coordinate in debug
                'map_clear_style': "visibility:visible;",
                'edit_geom': True,
                'min_zoom': 8,
                'wmts_capabilities_url': settings.WMTS_GETCAP,
                'wmts_layer': settings.WMTS_LAYER,
                'wmts_capabilities_url_alternative': settings.WMTS_GETCAP_ALTERNATIVE,
                'wmts_layer_alternative': settings.WMTS_LAYER_ALTERNATIVE,
                'administrative_entities_url': 'gpf:adm-entity-geojson',
            }),
            'administrative_entity': forms.Select(
                attrs = {'onchange' : "gpfMap.zoomToAdminEntity(this.options[this.selectedIndex].value);"
            }),
            'date_start': DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                    "locale": "fr",
                    "minDate": (datetime.datetime.today() + datetime.timedelta(days=int(settings.MIN_START_DELAY))).strftime('%Y/%m/%d')
                    }
                ).start_of('event days'),
            'date_end': DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                    "locale": "fr",
                    "minDate": (datetime.datetime.today() + datetime.timedelta(days=int(settings.MIN_START_DELAY))).strftime('%Y/%m/%d')
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
                    "search_prefix": "true",
                    "origins": "address",
                    "zipcode_field": "zipcode_permit",
                    "city_field": "city_permit",
                    "placeholder": "ex: Rue de la plaine",
                }),
        }


class ChangePermitRequestForm(forms.ModelForm):

    required_css_class = 'required'

    class Meta:

        model = PermitRequest
        exclude = []
        fields = [
            'company', 'project_owner', 'ended', 'archeotype', 'has_archeology', 'amount', 'paid', 'validated', 'sent', 'date_start', 'date_end',
            'date_end_work_announcement', 'date_end_work', 'date_request_created', 'road_marking_damaged',
            'is_green_area', 'invoice_to', 'sitetype',
            'description', 'administrative_entity', 'address', 'length', 'width', 'geom'
        ]
        help_texts = {
            'validated': "Par le secrétariat uniquement",
            'archeotype': "Zone archéologique observée au moment de la fouille",
            'has_archeology': "Zone archéologique détectée sur la base des géodonnées cantonales",
            'ended': "La fouille a-t-elle été contrôlée par le bureau STE ?",
        }
        widgets = {
            'geom': SitOpenLayersWidget(attrs={
                'map_width': '100%',
                'map_height': settings.OL_MAP_HEIGHT,
                'map_srid': 2056,
                'default_center': [2539057, 1181111],
                'default_zoom': 10,
                'display_raw': False, #show coordinate in debug
                'map_clear_style': "visibility:visible;",
                'edit_geom': False,
                'min_zoom': 6,
                'wmts_capabilities_url': settings.WMTS_GETCAP,
                'wmts_layer': settings.WMTS_LAYER,
                'wmts_capabilities_url_alternative': settings.WMTS_GETCAP_ALTERNATIVE,
                'wmts_layer_alternative': settings.WMTS_LAYER_ALTERNATIVE,
                'administrative_entities_url': 'gpf:adm-entity-geojson',
            }),
            'administrative_entity': forms.Select(
                attrs = {'onchange' : "gpfMap.zoomToAdminEntity(this.options[this.selectedIndex].value);"
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
                    "search_prefix": "true",
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
                    "search_prefix": "false",
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


class GenericActorForm(forms.ModelForm):

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
                    "search_prefix": "false",
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
                    "search_prefix": "false",
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
            'email': forms.TextInput(attrs={'placeholder': 'ex: permis-de-fouille@mapnv.ch'}),
        }
        labels = {
            'address': _("Address"),
            'phone_fixed': _("Phone"),
            'phone_mobile': _("Mobile phone"),
            'name': _("Last name"),
            'firstname': _("First name"),
            'zipcode': _("Zipcode"),
            'city': _("City"),
            'company_name': _("Company name"),
            'email': _("Email address"),
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
