from django.conf import settings
from django import forms
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import UserCreationForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis import forms as geoforms
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import json
from . import models, services, widgets
from bootstrap_datepicker_plus import DateTimePickerInput
from datetime import datetime, timedelta


def get_field_cls_for_property(prop):
    input_type_mapping = {
        models.WorksObjectProperty.INPUT_TYPE_TEXT: forms.CharField,
        models.WorksObjectProperty.INPUT_TYPE_CHECKBOX: forms.BooleanField,
        models.WorksObjectProperty.INPUT_TYPE_NUMBER: forms.FloatField,
        models.WorksObjectProperty.INPUT_TYPE_FILE: forms.FileField,
    }

    return input_type_mapping[prop.input_type]


class AdministrativeEntityForm(forms.Form):

    administrative_entity = forms.ModelChoiceField(queryset=models.PermitAdministrativeEntity.objects.none(),
                                                   label=_("Entité administrative"))

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)

        if self.instance:
            initial = {**kwargs.get('initial', {}), 'administrative_entity': self.instance.administrative_entity}
        else:
            initial = {}

        kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

        self.fields['administrative_entity'].queryset = services.get_administrative_entities()

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


class PermitAuthorUserForm(UserCreationForm):

    required_css_class = 'required'


class GenericAuthorForm(forms.ModelForm):

    required_css_class = 'required'

    class Meta:
        model = models.PermitAuthor
        exclude = ['user']
        help_texts = {
            'vat_number': 'Trouvez votre numéro <a href="https://www.bfs.admin.ch/bfs/fr/home/registres/registre-entreprises/numero-identification-entreprises.html" target="_blank">TVA</a>',
        }
        widgets = {
            'address': widgets.RemoteAutocompleteWidget(
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


class PermitRequestActorForm(forms.ModelForm):

    actor_fields = ['firstname', 'name', 'company_name', 'vat_number', 'address', 'address', 'city', 'phone',
                    'zipcode', 'email']

    name = forms.CharField( max_length=100, label=_('Nom'), widget=forms.TextInput(attrs={'placeholder': 'ex: Marcel', 'required': 'required'}))
    firstname = forms.CharField(max_length=100, label=_('Prénom'), widget=forms.TextInput(attrs={'placeholder': 'ex: Dupond', 'required': 'required'}))
    phone = forms.CharField(max_length=20, label=_('Téléphone'), widget=forms.TextInput(attrs={'placeholder': 'ex: 024 111 22 22', 'required': 'required'}))
    email = forms.EmailField(max_length=100, label=_('Email'), widget=forms.TextInput(attrs={'placeholder': 'ex: example@example.com', 'required': 'required'}))
    address = forms.CharField(max_length=100, label=_('Adresse'), widget= forms.TextInput(
            attrs={
                "data_remote_autocomplete": json.dumps({
                "apiurl": "https://api3.geo.admin.ch/rest/services/api/SearchServer?",
                "apiurl_detail": "https://api3.geo.admin.ch/rest/services/api/MapServer/ch.bfs.gebaeude_wohnungs_register/",
                "search_prefix": "false",
                "origins": "address",
                "zipcode_field": "zipcode",
                "city_field": "city",
                "placeholder": "ex: Place Pestalozzi 2 Yverdon",}),
                'required': 'required',
            }),
    )

    zipcode = forms.IntegerField(label=_('NPA'), widget=forms.NumberInput(attrs={'required': 'required'}))
    city = forms.CharField(max_length=100, label=_('Ville'), widget=forms.TextInput(attrs={'placeholder': 'ex: Yverdon', 'required': 'required'}))
    company_name = forms.CharField(required=False, label=_('Raison sociale'), max_length=100, widget=forms.TextInput(attrs={'placeholder': 'ex: Construction SA'}))
    vat_number = forms.CharField(required=False, label=_('Numéro TVA'), max_length=100,widget=forms.TextInput(attrs={'placeholder': 'ex: CHE-123.456.789'}))

    class Meta:
        model = models.PermitRequestActor
        fields = ['actor_type']
        widgets = {'actor_type': forms.Select(
                attrs={'readonly': 'readonly',}
            ),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')

        if instance and instance.pk:
            kwargs['initial'] = {**kwargs.get('initial', {}), **{
                **kwargs.get('initial', {}), **{field: getattr(instance.actor, field) for field in self.actor_fields},
                **{'actor_type': instance.actor_type}
            }}

        super().__init__(*args, **kwargs)

    @transaction.atomic
    def save(self, permit_request, commit=True):
        actor = self.instance.actor if self.instance.pk else None

        if not actor:
            actor = models.PermitActor.objects.create(
                **{field: self.cleaned_data.get(field) for field in self.actor_fields}
            )
        else:
            for field in self.actor_fields:
                setattr(actor, field, self.cleaned_data.get(field))
            actor.save()

        instance = super().save(commit=False)
        instance.actor = actor
        instance.permit_request = permit_request
        instance.save()

        return instance


class PermitRequestAdditionalInformationForm(forms.ModelForm):
    class Meta:
        model = models.PermitRequest
        fields = ['status', 'price', 'exemption', 'opposition', 'comment']
        widgets = {
            'exemption': forms.Textarea(attrs={'rows': 3}),
            'opposition': forms.Textarea(attrs={'rows': 3}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Prevent secretariat from putting back a request in draft status
        self.fields['status'].choices = [
            (status, label)
            for status, label in self.fields['status'].choices
            if status != models.PermitRequest.STATUS_DRAFT
        ]


# extend django gis osm openlayers widget
class GeometryWidget(geoforms.OSMWidget):

    template_name = 'geometrywidget/geometrywidget.html'
    map_srid = 2056

    @property
    def media(self):
        return forms.Media(
            css={'all': ('libs/js/openlayers6/ol.css',)},
            js=('libs/js/openlayers6/ol.js',
                'libs/js/proj4js/proj4-src.js',
                'customWidgets/GeometryWidget/geometrywidget.js'
                ))


class PermitRequestGeoTimeForm(forms.ModelForm):

    class Meta:
        model = models.PermitRequestGeoTime
        fields = ['starts_at', 'ends_at', 'comment', 'external_link', 'geom']
        widgets = {
            'geom': GeometryWidget(attrs={
                'map_width': '100%',
                'map_height': 400,
                'default_center': [2539057, 1181111],
                'default_zoom': 10,
                'display_raw': False,
                'edit_geom': True,
                'min_zoom': 8,
                'wmts_capabilities_url': settings.WMTS_GETCAP,
                'wmts_layer': settings.WMTS_LAYER,
                'wmts_capabilities_url_alternative': settings.WMTS_GETCAP_ALTERNATIVE,
                'wmts_layer_alternative': settings.WMTS_LAYER_ALTERNATIVE,
            }),
            'starts_at': DateTimePickerInput(
                  options={
                        "format": "DD/MM/YYYY HH:mm",
                        "locale": "fr",
                        "useCurrent": False,
                        "minDate": (datetime.today() +
                                    timedelta(days=int(settings.MIN_START_DELAY))).strftime('%Y/%m/%d')
                        }
                     ).start_of('event days'),
            'ends_at': DateTimePickerInput(
                  options={
                        "format": "DD/MM/YYYY  HH:mm",
                        "locale": "fr",
                        "useCurrent": False,
                        }
                    ).end_of('event days'),

        }


class PermitRequestValidationDepartmentSelectionForm(forms.Form):
    departments = forms.ModelMultipleChoiceField(
        queryset=models.PermitDepartment.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        label=_("Services chargés de la validation")
    )

    def __init__(self, instance, *args, **kwargs):
        self.permit_request = instance
        permit_request_ct = ContentType.objects.get_for_model(models.PermitRequest)
        validate_permission = Permission.objects.get(codename='validate_permit_request', content_type=permit_request_ct)
        permit_request_departments = models.PermitDepartment.objects.filter(
            administrative_entity=self.permit_request.administrative_entity,
            group__permissions=validate_permission
        ).distinct()
        kwargs["initial"] = dict(
            kwargs.get("initial", {}), departments=permit_request_departments.filter(is_default_validator=True)
        )

        super().__init__(*args, **kwargs)
        self.fields["departments"].queryset = permit_request_departments


class PermitRequestValidationForm(forms.ModelForm):
    class Meta:
        model = models.PermitRequestValidation
        fields = ("validation_status", "comment_before", "comment_during", "comment_after")
        widgets = {
            'comment_before': forms.Textarea(attrs={'rows': 3}),
            'comment_during': forms.Textarea(attrs={'rows': 3}),
            'comment_after': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show "----" instead of "en attente" for the default status
        self.fields["validation_status"].choices = [
            (value, label if value != models.PermitRequestValidation.STATUS_REQUESTED else "-" * 9)
            for value, label in self.fields["validation_status"].choices
        ]


class PermitRequestValidationPokeForm(forms.Form):
    def __init__(self, instance, request, *args, **kwargs):
        self.permit_request = instance
        self.request = request

        super().__init__(*args, **kwargs)

    def save(self):
        return services.send_validation_reminder(
            self.permit_request, absolute_uri_func=self.request.build_absolute_uri
        )


class PermitRequestClassifyForm(forms.ModelForm):
    # Status field is set as initial value when instanciating the form in the view
    status = forms.ChoiceField(choices=(
        (status, label)
        for status, label in models.PermitRequest.STATUS_CHOICES
        if status in [models.PermitRequest.STATUS_APPROVED, models.PermitRequest.STATUS_REJECTED]
    ), widget=forms.HiddenInput, disabled=True)

    class Meta:
        model = models.PermitRequest
        fields = ["status", "validation_pdf"]

    def save(self, commit=True):
        permit_request = super().save(commit=False)

        # ModelForm doesn't set the status because the field is disabled, so let's do it manually
        if self.cleaned_data["status"]:
            permit_request.status = self.cleaned_data["status"]

        permit_request.validated_at = timezone.now()

        if commit:
            permit_request.save()

        return permit_request
