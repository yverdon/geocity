from django import template
from django.shortcuts import render
from permits import forms


register = template.Library()

# @register.simple_tag
@register.inclusion_tag('permits/_permit_progressbar.html')
def permit_progressbar(permit_request, step):


    steps = {
        'AdministrativeEntityForm': {'state': 'done', 'name': 'Commune', 'number': 1, 'active': False}, # must have one item selected a least
        'WorksTypesForm': {'state': 'done', 'name': 'Travaux', 'number': 2, 'active': False}, # must have one item selected a least
        'WorksObjectsForm': {'state':'partial', 'name': 'Objets', 'number': 3 ,'active': False}, # must have one object by worktype selected at least
        'WorksObjectsPropertiesForm': {'state': 'partial', 'name': 'Détails', 'number': 4,'active': False}, # must be valid
        'WorksObjectsAppendicesForm': {'state': 'todo', 'name': 'Documents', 'number': 5,'active': False}, # must be valid
        'WorksContactForm': {'state': 'todo', 'name': 'Contacts', 'number': 6,'active': False}, # must be valid
        'SubmitForm': {'state': 'todo', 'name': 'Envoi', 'number': 7,'active': False}, # must be valid
    }

    if step in steps.keys():
        steps[step]['active'] = True


    if permit_request:

        # check validation state for properties
        form = forms.WorksObjectsPropertiesForm(instance=permit_request, enable_validation=True)
        if form.is_valid():
            steps['WorksObjectsPropertiesForm'] = True
        print(form.errors)
        # check validation state for appendices
        form = forms.WorksObjectsAppendicesForm(instance=permit_request, enable_validation=True)
        if form.is_valid():
            steps['WorksObjectsAppendicesForm'] = True

    steps_states = {
        'steps': steps
    }

    return steps_states
