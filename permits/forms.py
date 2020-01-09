from django import forms
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from . import models


class WorksTypesForm(forms.Form):
    types = forms.ModelMultipleChoiceField(
        queryset=models.WorksType.objects.all(), widget=forms.CheckboxSelectMultiple(), label=_("Types de travaux")
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)

        super().__init__(*args, **kwargs)

    def save(self):
        if not self.instance:
            return

        works_object_type_choices = models.WorksObjectTypeChoice.objects.filter(permit_request=self.instance)
        works_type_ids = set(works_object_type_choices.values_list('works_object_type__works_type_id', flat=True))
        selected_works_type_ids = set(obj.pk for obj in self.cleaned_data['types'])

        deleted_works_type_ids = works_type_ids - selected_works_type_ids
        works_object_type_choices.filter(works_object_type__works_type_id__in=deleted_works_type_ids).delete()


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
        works_object_types = [item for sublist in self.cleaned_data.values() for item in sublist]

        if not self.instance:
            new_works_object_type_ids = [obj.pk for obj in works_object_types]
        else:
            # Check which object type are new or have been removed. We can't just remove them all and recreate them
            # because there might be data related to these relations (eg. WorksObjectPropertyValue)
            works_object_type_choices = models.WorksObjectTypeChoice.objects.filter(permit_request=permit_request)
            works_object_type_ids = set(works_object_type_choices.values_list('works_object_type_id', flat=True))
            selected_object_type_ids = set(obj.pk for obj in works_object_types)

            deleted_works_object_type_ids = works_object_type_ids - selected_object_type_ids
            works_object_type_choices.filter(works_object_type_id__in=deleted_works_object_type_ids).delete()

            new_works_object_type_ids = selected_object_type_ids - works_object_type_ids

        for works_object_type_id in new_works_object_type_ids:
            models.WorksObjectTypeChoice.objects.create(
                permit_request=permit_request, works_object_type_id=works_object_type_id
            )

        return permit_request
