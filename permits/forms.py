from django import forms
from django.conf import settings
from django.contrib.gis import forms as geoforms
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from . import models, services
from gpf.models import Actor
from .widgets import RemoteAutocompleteWidget
from bootstrap_datepicker_plus import DatePickerInput
import datetime


def get_field_cls_for_property(prop):
    input_type_mapping = {
        models.WorksObjectProperty.INPUT_TYPE_TEXT: forms.CharField,
        models.WorksObjectProperty.INPUT_TYPE_CHECKBOX: forms.BooleanField,
        models.WorksObjectProperty.INPUT_TYPE_NUMBER: forms.IntegerField,
        models.WorksObjectProperty.INPUT_TYPE_FILE: forms.FileField,
    }

    return input_type_mapping[prop.input_type]


class AdministrativeEntityForm(forms.Form):
    administrative_entity = forms.ModelChoiceField(queryset=services.get_administrative_entities(), label=_("Commune"))

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)

        if self.instance:
            initial = {**kwargs.get('initial', {}), 'administrative_entity': self.instance.administrative_entity}
        else:
            initial = {}

        kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

    def save(self, author):
        if not self.instance:
            return models.PermitRequest.objects.create(
                administrative_entity=self.cleaned_data['administrative_entity'], author=author
            )
        else:
            services.set_administrative_entity(self.instance, self.cleaned_data['administrative_entity'])
            return self.instance


class WorksTypesForm(forms.Form):
    types = forms.ModelMultipleChoiceField(
        queryset=models.WorksType.objects.none(), widget=forms.CheckboxSelectMultiple(), label=_("Types de travaux")
    )

    def __init__(self, instance, *args, **kwargs):
        self.instance = instance

        kwargs['initial'] = {
            'types': services.get_permit_request_works_types(self.instance)
        } if self.instance else {}

        super().__init__(*args, **kwargs)

        self.fields['types'].queryset = services.get_works_types(self.instance.administrative_entity)

    def save(self):
        services.set_works_types(self.instance, self.cleaned_data['types'])


class WorksObjectsTypeChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.works_object.name


class WorksObjectsForm(forms.Form):
    prefix = 'works_objects'

    def __init__(self, instance, works_types, *args, **kwargs):
        self.instance = instance

        initial = {}
        for type_id, object_id in self.instance.works_object_types.values_list('works_type__id', 'id'):
            initial.setdefault(str(type_id), []).append(object_id)

        super().__init__(*args, **{**kwargs, 'initial': initial})

        for works_type in works_types.prefetch_related('works_object_types'):
            self.fields[str(works_type.pk)] = WorksObjectsTypeChoiceField(
                queryset=works_type.works_object_types.filter(
                    administrative_entities=self.instance.administrative_entity
                ).distinct(),
                widget=forms.CheckboxSelectMultiple(), label=works_type.name
            )

    @transaction.atomic
    def save(self):
        works_object_types = [item for sublist in self.cleaned_data.values() for item in sublist]

        services.set_works_object_types(self.instance, works_object_types)

        return self.instance


class PartialValidationMixin:
    def __init__(self, *args, **kwargs):
        # Set to `False` to disable required fields validation (useful to allow saving incomplete forms)
        self.enable_required = kwargs.pop('enable_required', True)
        super().__init__(*args, **kwargs)


class WorksObjectsPropertiesForm(PartialValidationMixin, forms.Form):
    prefix = 'properties'

    def __init__(self, instance, *args, **kwargs):
        self.instance = instance
        disable_fields = kwargs.pop('disable_fields', False)

        # Compute initial values for fields
        initial = {}
        prop_values = self.get_values()
        for prop_value in prop_values:
            initial[
                self.get_field_name(prop_value.works_object_type_choice.works_object_type, prop_value.property)
            ] = services.get_property_value(prop_value)

        kwargs['initial'] = {**initial, **kwargs.get('initial', {})}

        super().__init__(*args, **kwargs)

        # Create a field for each property
        for works_object_type, prop in self.get_properties():
            field_name = self.get_field_name(works_object_type, prop)
            self.fields[field_name] = self.field_for_property(prop)

        if disable_fields:
            for field in self.fields.values():
                field.disabled = True


    def get_fields_by_object_type(self):
        """
        Return a list of tuples `(WorksObjectType, List[Field])` for each object type and their properties.
        """
        return [
            (object_type, [self[self.get_field_name(object_type, prop)] for prop in props])
            for object_type, props in self.get_properties_by_object_type()
        ]

    def get_properties_by_object_type(self):
        """
        Return a list of tuples `(WorksObjectType, List[WorksObjectTypeProperty])` for the object-types selected in the
        current permit request.
        """
        return services.get_properties(self.instance)

    def get_properties(self):
        """
        Return a list of tuples `(WorksObjectType, WorksObjectTypeProperty)` for the current permit request. They're
        used to create the form fields.
        """
        return services.get_permit_request_properties(self.instance)

    def get_values(self):
        """
        Return a `WorksObjectPropertyValue` objects for the current permit request. They're used to set the initial
        value of the form fields.
        """
        return services.get_properties_values(self.instance)

    def get_field_name(self, works_object_type, prop):
        return "{}_{}".format(works_object_type.pk, prop.pk)

    def field_for_property(self, prop):
        """
        Return a Field instance for the given property. The specific class of the field is defined by
        `get_field_cls_for_property`.
        """
        field_class = get_field_cls_for_property(prop)
        return field_class(**self.get_field_kwargs(prop))

    def get_field_kwargs(self, prop):
        """
        Return the options used when instanciating the field for the given `prop`.
        """
        return {
            'required': self.enable_required and prop.is_mandatory,
            'label': prop.name
        }

    def save(self):
        for works_object_type, prop in self.get_properties():
            services.set_object_property_value(
                permit_request=self.instance,
                object_type=works_object_type,
                prop=prop,
                value=self.cleaned_data[self.get_field_name(works_object_type, prop)]
            )


class WorksObjectsAppendicesForm(WorksObjectsPropertiesForm):
    prefix = 'appendices'

    def get_properties_by_object_type(self):
        return services.get_appendices(self.instance)

    def get_properties(self):
        return services.get_permit_request_appendices(self.instance)

    def get_values(self):
        return services.get_appendices_values(self.instance)

    def get_field_kwargs(self, prop):
        return {**super().get_field_kwargs(prop), **{'widget': forms.ClearableFileInput}}


class GenericActorForm(forms.ModelForm):

    description = forms.CharField(max_length=128)
    actor_type  =  forms.ChoiceField(choices=models.ACTOR_TYPE_CHOICES, disabled=True)

    class Meta:
        model = Actor
        exclude = ['user']
        fields = ['actor_type', 'name', 'firstname', 'email', 'company_name', 'address', 'zipcode', 'city', 'phone_fixed', 'phone_mobile']
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
            'email': forms.TextInput(attrs={'placeholder': 'ex: monemail@monemail.com'}),
        }


class SitOpenLayersWidget(geoforms.OSMWidget):

    template_name = 'permits/openlayers/openlayers_multigeom.html'
    map_srid = 2056

    @property
    def media(self):
        return forms.Media(
            css={'all': ('libs/js/openlayers6/ol.css',)},
            js=('libs/js/openlayers6/ol.js',
                'libs/js/proj4js/proj4-src.js',
                'customWidgets/sitMapWidget/sitMapWidgetGeometryCollection.js'
                ))


class PermitRequestGeoTimeForm(forms.ModelForm):

    class Meta:
        model = models.PermitRequestGeoTime
        fields = ['datetime_start', 'datetime_end', 'description','external_link', 'geom']
        widgets = {
            'geom': SitOpenLayersWidget(attrs={
                'map_width': '100%',
                'map_height': 400,
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
            'datetime_start': DatePickerInput(
                options={
                    "format": "DD/MM/YYYY HH:MM",
                    "locale": "fr",
                    "minDate": (datetime.datetime.today() + datetime.timedelta(days=int(settings.MIN_START_DELAY))).strftime('%Y/%m/%d')
                    }
                ).start_of('event days'),
            'datetime_end': DatePickerInput(
                options={
                    "format": "DD/MM/YYYY  HH:MM",
                    "locale": "fr",
                    "minDate": (datetime.datetime.today() + datetime.timedelta(days=int(settings.MIN_START_DELAY))).strftime('%Y/%m/%d')
                    }
                ).end_of('event days'),

        }
