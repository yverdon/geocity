from django import template
from django.shortcuts import render
from permits import forms, services
from django.urls import reverse
from django.forms import modelformset_factory
from gpf.models import Actor


register = template.Library()

# @register.simple_tag
@register.inclusion_tag('permits/_permit_progressbar.html')
def permit_progressbar(permit_request, step):


    steps = {
        # TODO: handle the wrong edit in location
        'AdministrativeEntityForm': {'state': 'done', 'name': 'Localisation', 'number': 1, 'current': 'inactive-step', 'enabled': 'enabled-step',
            'url': reverse('permits:permit_request_select_administrative_entity', kwargs={'permit_request_id': permit_request.pk}),}, # must have one item selected a least
        'WorksTypesForm': {'state': 'todo', 'name': 'Travaux', 'number': 2, 'current': 'inactive-step', 'enabled': 'disabled-step',
            'url': reverse('permits:permit_request_select_types', kwargs={'permit_request_id': permit_request.pk}),}, # must have one item selected a least
        'WorksObjectsForm': {'state':'todo', 'name': 'Objets', 'number': 3 , 'current': 'inactive-step', 'enabled': 'disabled-step',
            'url': reverse('permits:permit_request_select_objects', kwargs={'permit_request_id': permit_request.pk}),}, # must have one object by worktype selected at least
        'WorksObjectsPropertiesForm': {'state': 'todo', 'name': 'Détails', 'number': 4, 'current': 'inactive-step', 'disabled': 'disabled-step',
            'url': reverse('permits:permit_request_properties', kwargs={'permit_request_id': permit_request.pk}),}, # must be valid
        'WorksObjectsAppendicesForm': {'state': 'todo', 'name': 'Documents', 'number': 5, 'current': 'inactive-step', 'disabled': 'disabled-step',
            'url': reverse('permits:permit_request_appendices', kwargs={'permit_request_id': permit_request.pk}),}, # must be valid
        'WorksContactForm': {'state': 'todo', 'name': 'Contacts', 'number': 6, 'current': 'inactive-step', 'enabled': 'disabled-step',
            'url': reverse('permits:permit_request_actors', kwargs={'permit_request_id': permit_request.pk} if permit_request else {}),}, # must be valid
        'SubmitForm': {'state': 'todo', 'name': 'Envoi', 'number': 7, 'current': 'disabled-step', 'enabled': 'disabled-step',
            'url': reverse('permits:permit_request_submit', kwargs={'permit_request_id': permit_request.pk} if permit_request else {}),}, # must be valid
    }


    if step in steps.keys():
        steps[step]['current'] = 'active-step'


    if permit_request:

        form_properties = forms.WorksObjectsPropertiesForm(instance=permit_request, enable_required=True)
        form_appendices = forms.WorksObjectsAppendicesForm(instance=permit_request, enable_required=True, data={})
        GenericActorFormSet = modelformset_factory(Actor, form=forms.GenericActorForm)
        queryset = permit_request.actors.all()
        actors_formset_properties = GenericActorFormSet(queryset=queryset, data={})

        if permit_request.works_object_types.exists():

            steps['WorksTypesForm']['state'] = 'done'

        if permit_request.worksobjecttypechoice_set.exists():

            steps['WorksObjectsForm']['state'] = 'done'
            steps['WorksTypesForm']['state'] = 'done'
            steps['WorksObjectsForm']['enabled'] = 'enabled-step'
            steps['WorksTypesForm']['enabled'] = 'enabled-step'
            steps['WorksObjectsPropertiesForm']['enabled'] = 'enabled-step'
            steps['WorksObjectsAppendicesForm']['enabled'] = 'enabled-step'
            steps['WorksContactForm']['enabled'] = 'enabled-step'
            steps['SubmitForm']['enabled'] = 'enabled-step'

            form_proprties_count = len(form_properties.fields)
            correct_form_properties = len([array for key, array in form_properties.initial.items() if array])
            form_properties_message = ''
            if form_properties.initial == {}:
                steps['WorksObjectsPropertiesForm']['state'] = 'partial'
                steps['WorksObjectsPropertiesForm']['name']  += '(0/' + str(form_proprties_count) + ')'

            elif form_proprties_count - correct_form_properties > 0:
                steps['WorksObjectsPropertiesForm']['state'] = 'partial'
                steps['WorksObjectsPropertiesForm']['name']  += '(' + str(form_proprties_count -  correct_form_properties) + '/' + str(form_proprties_count) + ')'

            else:
                steps['WorksObjectsPropertiesForm']['state'] = 'done'

            if form_appendices.is_valid():
                steps['WorksObjectsAppendicesForm']['state'] = 'done'
            else:
                steps['WorksObjectsAppendicesForm']['partial'] = 'partial'



            # TODO: instantiate model formset correctly
            # if actors_formset_properties.is_valid():
            #     steps['WorksContactForm']['state'] = 'done'
            # else:
            #     steps['WorksContactForm']['partial'] = 'partial'

        else:
            steps['WorksTypesForm']['enabled'] = 'enabled-step'
            steps['WorksObjectsPropertiesForm']['enabled'] = 'disabled-step'
            steps['WorksObjectsAppendicesForm']['enabled'] = 'disabled-step'
            steps['WorksContactForm']['enabled'] = 'disabled-step'
            steps['SubmitForm']['enabled'] = 'disabled-step'

            steps['WorksObjectsPropertiesForm']['state'] = 'todo'
            steps['WorksObjectsAppendicesForm']['partial'] = 'todo'


    steps_states = {
        'steps': steps,
    }

    return steps_states
