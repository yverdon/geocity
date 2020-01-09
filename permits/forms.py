from django import forms
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from . import models


class WorksTypesForm(forms.Form):
    types = forms.ModelMultipleChoiceField(
        queryset=models.WorksType.objects.all(), widget=forms.CheckboxSelectMultiple(), label=_("Types de travaux")
    )


class WorksObjectsTypeChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.works_object.name


class WorksObjectsForm(forms.Form):
    prefix = 'works_objects'

    def __init__(self, works_types, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)

        super().__init__(*args, **kwargs)

        for works_type in works_types:
            self.fields[str(works_type.pk)] = WorksObjectsTypeChoiceField(
                queryset=models.WorksObjectType.objects.filter(works_type=works_type),
                widget=forms.CheckboxSelectMultiple(), label=works_type.name
            )

    @transaction.atomic
    def save(self):
        permit_request = self.instance or models.PermitRequest.objects.create()

        if not self.instance:
            works_objects_types = [item for sublist in self.cleaned_data.values() for item in sublist]
            for works_object_type in works_objects_types:
                models.WorksObjectTypeChoice.objects.create(
                    permit_request=permit_request, works_object_type=works_object_type
                )
        else:
            # TODO create inexistent WorksObjectTypeChoice
            pass

        return permit_request
