from django import forms
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from . import models, services


def get_field_cls_for_property(prop):
    input_type_mapping = {
        models.WorksObjectProperty.INPUT_TYPE_TEXT: forms.CharField,
        models.WorksObjectProperty.INPUT_TYPE_CHECKBOX: forms.BooleanField,
        models.WorksObjectProperty.INPUT_TYPE_NUMBER: forms.IntegerField,
        models.WorksObjectProperty.INPUT_TYPE_FILE: forms.FileField,
    }

    return input_type_mapping[prop.input_type]


class WorksTypesForm(forms.Form):
    types = forms.ModelMultipleChoiceField(
        queryset=services.get_works_types(), widget=forms.CheckboxSelectMultiple(), label=_("Types de travaux")
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)

        kwargs['initial'] = {
            'types': services.get_permit_request_works_types(self.instance)
        } if self.instance else {}

        super().__init__(*args, **kwargs)

    def save(self):
        if not self.instance:
            return

        services.set_works_types(self.instance, self.cleaned_data['types'])


class WorksObjectsTypeChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.works_object.name


class WorksObjectsForm(forms.Form):
    prefix = 'works_objects'

    def __init__(self, works_types, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)

        initial = {}

        if self.instance:
            for type_id, object_id in self.instance.works_objects_types.values_list('works_type__id', 'id'):
                initial.setdefault(str(type_id), []).append(object_id)

        super().__init__(*args, **{**kwargs, 'initial': initial})

        for works_type in works_types:
            self.fields[str(works_type.pk)] = WorksObjectsTypeChoiceField(
                queryset=models.WorksObjectType.objects.filter(works_type=works_type),
                widget=forms.CheckboxSelectMultiple(), label=works_type.name
            )

    @transaction.atomic
    def save(self):
        permit_request = self.instance or models.PermitRequest.objects.create()
        works_object_types = [item for sublist in self.cleaned_data.values() for item in sublist]

        services.set_works_object_types(permit_request, works_object_types)

        return permit_request


class PartialValidationMixin:
    def __init__(self, *args, **kwargs):
        # Set to `False` to disable required fields validation (useful to allow saving incomplete forms)
        self.enable_validation = kwargs.pop('enable_validation', True)
        super().__init__(*args, **kwargs)


class WorksObjectsPropertiesForm(PartialValidationMixin, forms.Form):
    prefix = 'properties'

    def __init__(self, instance, *args, **kwargs):
        self.instance = instance

        # Compute initial values for fields
        initial = {}
        prop_values = self.get_values()
        for prop_value in prop_values:
            initial[
                self.get_field_name(prop_value.works_object_type_choice.works_object_type, prop_value.property)
            ] = prop_value.value['val']

        kwargs['initial'] = {**initial, **kwargs.get('initial', {})}

        super().__init__(*args, **kwargs)

        # Create field for each property
        for works_object_type, prop in self.get_properties():
            field_name = self.get_field_name(works_object_type, prop)
            self.fields[field_name] = self.get_field_for_property(prop)

    def get_properties(self):
        return services.get_permit_request_properties(self.instance)

    def get_values(self):
        return services.get_properties_values(self.instance)

    def get_field_name(self, works_object_type, prop):
        return "{}_{}".format(works_object_type.pk, prop.pk)

    def get_field_for_property(self, prop):
        field_class = get_field_cls_for_property(prop)
        return field_class(
            required=self.enable_validation and prop.is_mandatory,
            label=prop.name
        )

    def save(self):
        for works_object_type, prop in services.get_permit_request_properties(self.instance):
            services.set_object_property_value(
                permit_request=self.instance,
                object_type=works_object_type,
                prop=prop,
                value=self.cleaned_data[self.get_field_name(works_object_type, prop)]
            )


class WorksObjectsAppendicesForm(WorksObjectsPropertiesForm):
    prefix = 'appendices'

    def get_properties(self):
        return services.get_permit_request_appendices(self.instance)

    def get_values(self):
        return services.get_appendices_values(self.instance)
