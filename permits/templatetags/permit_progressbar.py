from django import template
from django.shortcuts import render
from permits import forms


register = template.Library()

# @register.simple_tag
@register.inclusion_tag('permits/_permit_progressbar.html')
def permit_progressbar(permit_request, step):


    steps = {
        'WorksTypesForm': {'state': 'done', 'name': 'Types', 'number': 1, 'current': step}, # must have one item selected a least
        'WorksObjectsForm': {'state':'partial', 'name': 'Objets', 'number': 2 ,'current': step}, # must have one object by worktype selected at least
        'WorksObjectsPropertiesForm': {'state': 'partial', 'name': 'Détails', 'number': 3,'current': step}, # must be valid
        'WorksObjectsAppendicesForm': {'state': 'todo', 'name': 'Documents', 'number': 4,'current': step}, # must be valid
    }

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
