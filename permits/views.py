import mimetypes
import urllib.parse
import os
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.db import transaction
from django.forms import modelformset_factory
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from gpf.forms import ActorForm
from gpf.models import Actor

from . import forms, models, services, tables, filters
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView


def user_has_actor(user):
    try:
        user.actor
    except Actor.DoesNotExist:
        return False

    return True


@login_required
def permit_request_redirect(request, permit_request_id):
    return redirect('permits:permit_request_select_administrative_entity', permit_request_id=permit_request_id)


@login_required
@user_passes_test(user_has_actor)
def permit_request_select_administrative_entity(request, permit_request_id=None):
    if permit_request_id:
        permit_request = services.get_permit_request_for_user_or_404(request.user, permit_request_id)
    else:
        permit_request = None

    if request.method == 'POST':
        administrative_entity_form = forms.AdministrativeEntityForm(
            instance=permit_request, data=request.POST
        )

        if administrative_entity_form.is_valid():
            permit_request = administrative_entity_form.save(author=request.user.actor)

            return redirect(
                reverse('permits:permit_request_select_types', kwargs={'permit_request_id': permit_request.pk})
            )
    else:
        administrative_entity_form = forms.AdministrativeEntityForm(instance=permit_request)

    return render(request, "permits/permit_request_select_administrative_entity.html", {
        'form': administrative_entity_form,
        'permit_request': permit_request,
    })


@login_required
def permit_request_select_types(request, permit_request_id):
    """
    Step to select works types (eg. demolition). No permit request is created at this step since we only store (works
    object, works type) couples in the database.
    """
    permit_request = services.get_permit_request_for_user_or_404(request.user, permit_request_id)

    if request.method == 'POST':
        works_types_form = forms.WorksTypesForm(data=request.POST, instance=permit_request)

        if works_types_form.is_valid():
            works_types_form.save()
            redirect_kwargs = {'permit_request_id': permit_request_id}

            return redirect(
                reverse('permits:permit_request_select_objects', kwargs=redirect_kwargs)
                + '?' + urllib.parse.urlencode({
                    'types': [obj.pk for obj in works_types_form.cleaned_data['types']]
                }, doseq=True)
            )
    else:
        works_types_form = forms.WorksTypesForm(instance=permit_request)

    return render(request, "permits/permit_request_select_types.html", {
        'works_types_form': works_types_form,
        'permit_request': permit_request
    })


@login_required
def permit_request_select_objects(request, permit_request_id):
    """
    Step to select works objects. This view supports either editing an existing permit request (if `permit_request_id`
    is set) or creating a new permit request.
    """
    permit_request = services.get_permit_request_for_user_or_404(request.user, permit_request_id)

    if request.GET:
        works_types_form = forms.WorksTypesForm(data=request.GET, instance=permit_request)
        if not works_types_form.is_valid():
            return redirect('permits:permit_request_select_types', permit_request_id=permit_request.pk)
        works_types = works_types_form.cleaned_data['types']
    else:
        if not permit_request.works_object_types.exists():
            return redirect('permits:permit_request_select_types', permit_request_id=permit_request.pk)

        works_types = models.WorksType.objects.none()

    # Add the permit request works types to the ones in the querystring
    works_types = works_types.union(services.get_permit_request_works_types(permit_request)).distinct()

    if request.method == 'POST':
        works_objects_form = forms.WorksObjectsForm(
            data=request.POST, instance=permit_request, works_types=works_types
        )

        if works_objects_form.is_valid():
            permit_request = works_objects_form.save()
            return redirect('permits:permit_request_properties', permit_request_id=permit_request.pk)
    else:
        works_objects_form = forms.WorksObjectsForm(instance=permit_request, works_types=works_types)

    return render(request, "permits/permit_request_select_objects.html", {
        'works_objects_form': works_objects_form,
        'permit_request': permit_request
    })


@login_required
def permit_request_properties(request, permit_request_id):
    """
    Step to input properties values for the given permit request.
    """
    permit_request = services.get_permit_request_for_user_or_404(request.user, permit_request_id)

    if request.method == 'POST':
        # Disable `required` fields validation to allow partial save
        form = forms.WorksObjectsPropertiesForm(instance=permit_request, data=request.POST, enable_required=False)

        if form.is_valid():
            form.save()
            return redirect('permits:permit_request_appendices', permit_request_id=permit_request.pk)
    else:
        form = forms.WorksObjectsPropertiesForm(instance=permit_request, enable_required=False)

    fields_by_object_type = form.get_fields_by_object_type()

    return render(request, "permits/permit_request_properties.html", {
        'permit_request': permit_request,
        'object_types': fields_by_object_type,
    })


@login_required
def permit_request_appendices(request, permit_request_id):
    """
    Step to upload appendices for the given permit request.
    """
    permit_request = services.get_permit_request_for_user_or_404(request.user, permit_request_id)

    if request.method == 'POST':
        form = forms.WorksObjectsAppendicesForm(
            instance=permit_request, data=request.POST, files=request.FILES, enable_required=False
        )

        if form.is_valid():
            form.save()
            return redirect('permits:permit_request_actors', permit_request_id=permit_request.pk)
    else:
        form = forms.WorksObjectsAppendicesForm(instance=permit_request, enable_required=False)

    fields_by_object_type = form.get_fields_by_object_type()

    return render(request, "permits/permit_request_appendices.html", {
        'permit_request': permit_request,
        'object_types': fields_by_object_type,
    })


@login_required
def permit_request_actors(request, permit_request_id):
    permit_request = services.get_permit_request_for_user_or_404(request.user, permit_request_id)
    GenericActorFormSet = modelformset_factory(Actor, form=ActorForm, extra=0)
    queryset = permit_request.actors.all()

    if request.method == 'POST':
        formset = GenericActorFormSet(request.POST, request.FILES, queryset=queryset)

        if formset.is_valid():
            actors = []
            with transaction.atomic():
                for form in formset:
                    actors.append(form.save())
                permit_request.actors.set(actors)

            return redirect('permits:permit_request_summary', permit_request_id=permit_request.pk)
    else:
        formset = GenericActorFormSet(queryset=queryset)

    return render(request, "permits/permit_request_actors.html", {
        'formset': formset,
        'permit_request': permit_request
    })


@login_required
def permit_request_media_download(request, property_value_id):
    """
    Send the file referenced by the given property value.
    """
    # TODO allow other users to access the uploaded media (eg. services that will validate the request)
    property_value = get_object_or_404(
        models.WorksObjectPropertyValue.objects.filter(property__input_type=models.WorksObjectProperty.INPUT_TYPE_FILE),
        pk=property_value_id,
        works_object_type_choice__permit_request__author=request.user.actor
    )
    file = services.get_property_value(property_value)
    mime_type, encoding = mimetypes.guess_type(file.name)

    return StreamingHttpResponse(file, content_type=mime_type)


@method_decorator(login_required, name="dispatch")
class PermitRequestListExternsView(SingleTableMixin, FilterView):

    paginate_by = int(os.environ['PAGINATE_BY'])
    table_class = tables.PermitRequestTableExterns
    model = models.PermitRequest
    template_name = 'permits/permit_requests_list.html'
    filterset_class = filters.PermitRequestFilterExterns

    def get_queryset(self):
        return models.PermitRequest.objects.filter(author=Actor.objects.get(user=self.request.user))


@login_required
def permit_request_submit(request, permit_request_id):
    permit_request = services.get_permit_request_for_user_or_404(request.user, permit_request_id)

    if request.method == 'POST':
            permit_request.status = models.PermitRequest.STATUS_SUBMITTED
            permit_request.save()

            return redirect('permits:permit_requests_list')

    return render(request, "permits/permit_request_submit.html", {
        'permit_request': permit_request,
    })


@login_required
def permit_request_delete(request, permit_request_id):

    permit_request = services.get_permit_request_for_user_or_404(request.user, permit_request_id)

    if request.method == 'POST':

            permit_request.delete()

            return redirect('permits:permit_requests_list')


    return render(request, "permits/permit_request_delete.html", {
        'permit_request': permit_request
    })
