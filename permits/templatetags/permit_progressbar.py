from django import template
from django.shortcuts import render
from permits import forms


register = template.Library()

# @register.simple_tag
@register.inclusion_tag('permits/_permit_progressbar.html')
def permit_progressbar(permit_request, step):


    steps_states = {
        'current_step': step,
        'WorksTypesForm': False, # must have one item selected a least
        'WorksObjectsForm': False, # must have one object by worktype selected at least
        'WorksObjectsPropertiesForm': False, # must be valid
        'WorksObjectsAppendicesForm': False, # must be valid
    }

    if permit_request:

        # check validation state for properties
        form = forms.WorksObjectsPropertiesForm(instance=permit_request, enable_validation=True)
        if form.is_valid():
            step_states['WorksObjectsPropertiesForm'] = True
        print(form.errors)
        # check validation state for appendices
        form = forms.WorksObjectsAppendicesForm(instance=permit_request, enable_validation=True)
        if form.is_valid():
            step_states['WorksObjectsAppendicesForm'] = True



    return steps_states
