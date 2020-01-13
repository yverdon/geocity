import urllib.parse

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from . import forms, models


def permit_request_select_types(request, permit_request_id=None):
    if permit_request_id:
        permit_request = get_object_or_404(models.PermitRequest, pk=permit_request_id)
    else:
        permit_request = None

    if request.method == 'POST':
        works_types_form = forms.WorksTypesForm(request.POST, instance=permit_request)

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
        works_types_form = forms.WorksTypesForm(instance=permit_request)

    return render(request, "permits/permit_request_types.html", {
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
        works_types += [works_object_type.works_type for works_object_type in permit_request.works_objects_types.all()]
        works_types_form = None
    else:
        permit_request = None

    if request.method == 'POST':
        works_objects_form = forms.WorksObjectsForm(
            works_types, data=request.POST, instance=permit_request
        )

        if works_objects_form.is_valid():
            permit_request = works_objects_form.save()
            return redirect('permits:permit_request_properties', permit_request_id=permit_request.pk)
    else:
        works_objects_form = forms.WorksObjectsForm(works_types, instance=permit_request)

    return render(request, "permits/permit_request_select_objects.html", {
        'works_types_form': works_types_form,
        'works_objects_form': works_objects_form,
        'permit_request': permit_request
    })


def permit_request_properties(request, permit_request_id=None):
    permit_request = get_object_or_404(models.PermitRequest, pk=permit_request_id)

    if request.method == 'POST':
        form = forms.WorksObjectsPropertiesForm(instance=permit_request, data=request.POST, enable_validation=False)

        if form.is_valid():
            form.save()
            return redirect(reverse('permits:permit_request_appendices', permit_request_id=permit_request.pk))
    else:
        form = forms.WorksObjectsPropertiesForm(instance=permit_request, enable_validation=False)

    works_objects_types = permit_request.works_objects_types.all()
    fields_by_object_type = [
        (object_type, [form[form.get_field_name(object_type, prop)] for prop in object_type.properties.all()])
        for object_type in works_objects_types
    ]

    return render(request, "permits/permit_request_properties.html", {
        'permit_request': permit_request,
        'form': form,
        'objects_types': fields_by_object_type,
    })
