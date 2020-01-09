import urllib.parse

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from . import forms, models


def permit_request_select_types(request, permit_request_id=None):
    if permit_request_id:
        permit_request = get_object_or_404(models.PermitRequest, pk=permit_request_id)
        initial = {
            'types': [
                works_object_type.works_type for works_object_type in permit_request.works_objects_types.all()
            ]
        }
    else:
        initial = {}
        permit_request = None

    if request.method == 'POST':
        works_types_form = forms.WorksTypesForm(request.POST, initial=initial, instance=permit_request)

        if works_types_form.is_valid():
            works_types_form.save()
            redirect_kwargs = {'permit_request_id': permit_request_id} if permit_request_id else {}

            return redirect(
                reverse('permits:permit_request_select_objects', kwargs=redirect_kwargs)
                + '?' + urllib.parse.urlencode({
                    'types': [obj.pk for obj in works_types_form.cleaned_data['types']]
                }, doseq=True)
            )
    else:
        works_types_form = forms.WorksTypesForm(initial=initial, instance=permit_request)

    return render(request, "permits/permit_request_new.html", {
        'works_types_form': works_types_form,
        'permit_request': permit_request
    })


def permit_request_select_objects(request, permit_request_id=None):
    if not request.GET and not permit_request_id:
        return redirect('permits:permit_request_select_types')
    elif request.GET:
        works_types_form = forms.WorksTypesForm(request.GET)
        if not works_types_form.is_valid():
            return redirect('permits:permit_request_select_types')
        works_types = list(works_types_form.cleaned_data['types'].prefetch_related('works_objects'))
    else:
        works_types = []

    if permit_request_id:
        permit_request = get_object_or_404(models.PermitRequest, pk=permit_request_id)
        initial = {}
        for type_id, object_id in permit_request.works_objects_types.values_list('works_type__id', 'id'):
            initial.setdefault(str(type_id), []).append(object_id)

        works_types += [works_object_type.works_type for works_object_type in permit_request.works_objects_types.all()]
        works_types_form = None
    else:
        initial = {}
        permit_request = None

    if request.method == 'POST':
        works_objects_form = forms.WorksObjectsForm(
            works_types, data=request.POST, initial=initial, instance=permit_request
        )

        if works_objects_form.is_valid():
            permit_request = works_objects_form.save()
            return redirect('permits:permit_request_properties', permit_request_id=permit_request.pk)
    else:
        works_objects_form = forms.WorksObjectsForm(works_types, initial=initial)

    return render(request, "permits/permit_request_select_objects.html", {
        'works_types_form': works_types_form,
        'works_objects_form': works_objects_form,
        'permit_request': permit_request
    })


def permit_request_properties(request, permit_request_id=None):
    permit_request = get_object_or_404(models.PermitRequest, pk=permit_request_id)
    return render(request, "permits/permit_request_properties.html", {'permit_request': permit_request})
