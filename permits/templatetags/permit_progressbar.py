from django import template
from django.shortcuts import render
from permits import forms, services
from django.urls import reverse


register = template.Library()

# @register.simple_tag
@register.inclusion_tag('permits/_permit_progressbar.html')
def permit_progressbar(permit_request, step):


    steps = {
        'WorksTypesForm': {'state': 'todo', 'name': 'Travaux', 'number': 1, 'current': 'inactive-step', 'enabled': 'disabled-step',
            'url': reverse('permits:permit_request_select_types', kwargs={'permit_request_id': permit_request.pk}),}, # must have one item selected a least
        'WorksObjectsForm': {'state':'todo', 'name': 'Objets', 'number': 2 , 'current': 'inactive-step', 'enabled': 'disabled-step',
            'url': reverse('permits:permit_request_select_objects', kwargs={'permit_request_id': permit_request.pk}),}, # must have one object by worktype selected at least
        'WorksObjectsPropertiesForm': {'state': 'todo', 'name': 'Détails', 'number': 3, 'current': 'inactive-step', 'disabled': 'enabled-step',
            'url': reverse('permits:permit_request_properties', kwargs={'permit_request_id': permit_request.pk}),}, # must be valid
        'WorksObjectsAppendicesForm': {'state': 'todo', 'name': 'Documents', 'number': 4, 'current': 'inactive-step', 'disabled': 'enabled-step',
            'url': reverse('permits:permit_request_appendices', kwargs={'permit_request_id': permit_request.pk}),}, # must be valid
        'WorksContactForm': {'state': 'todo', 'name': 'Contacts', 'number': 5, 'current': 'inactive-step', 'enabled': 'disabled-step',
            'url': reverse('permits:permit_request_select_administrative_entity', kwargs={'permit_request_id': permit_request.pk} if permit_request else {}),}, # must be valid
        'SubmitForm': {'state': 'todo', 'name': 'Envoi', 'number': 6, 'current': 'disabled-step', 'enabled': 'disabled-step',
            'url': reverse('permits:permit_request_select_administrative_entity', kwargs={'permit_request_id': permit_request.pk} if permit_request else {}),}, # must be valid
    }


    if step in steps.keys():
        steps[step]['current'] = 'active-step'


    if permit_request:

        # check validation state for properties
        form = forms.WorksObjectsPropertiesForm(instance=permit_request, enable_required=True)

        if form.is_valid():
            steps['WorksObjectsPropertiesForm']['state'] = 'done'
        else:
            steps['WorksObjectsPropertiesForm']['state'] = 'partial'

        # check validation state for appendices
        form = forms.WorksObjectsAppendicesForm(instance=permit_request, enable_required=True)
        if form.is_valid():
            steps['WorksObjectsAppendicesForm']['state'] = 'done'
        else:
            steps['WorksObjectsAppendicesForm']['partial'] = 'partial'

        if permit_request.works_object_types.exists():

            steps['WorksTypesForm']['enabled'] = 'enabled-step'
            steps['WorksObjectsForm']['enabled'] = 'enabled-step'

        if permit_request.worksobjecttypechoice_set.exists():

            steps['WorksObjectsPropertiesForm']['enabled'] = 'enabled-step'
            steps['WorksObjectsAppendicesForm']['enabled'] = 'enabled-step'
            steps['WorksContactForm']['enabled'] = 'enabled-step'
            steps['SubmitForm']['enabled'] = 'enabled-step'

    steps_states = {
        'steps': steps
    }

    return steps_states
