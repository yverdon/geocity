import os, datetime, json
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect,HttpResponse, FileResponse,JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import DeleteView, FormView
from django.urls import reverse_lazy
from django.forms import formset_factory, inlineformset_factory
from .filters import PermitRequestFilter, PermitRequestFilterExterns
from .forms import AddPermitRequestForm, ChangePermitRequestForm
from .forms import ActorForm, CompanyForm, ValidationForm, DocumentForm, EndWorkForm, companyUserAddForm, GenericActorForm
from .models import Actor, Archelogy, PermitRequest, Validation, Department, Document, AdministrativeEntity
from .tables import PermitRequestTable, PermitRequestTableExterns, PermitExportTable
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView
from django_tables2.export.views import ExportMixin
import gpf.sendmail, gpf.print
from .helpers import *
from uuid import uuid4 as uuid
from django.views.generic.list import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from django.contrib import messages
from threading import Thread
import time


@login_required
def permitRequestAdd(request, project_owner_id):


    if request.method == 'POST':

        permit_form = AddPermitRequestForm(request.POST, request.FILES)

        # if the request is filled by intern employees, the user login is not
        # linked to a company, thus, we add an "unlinked company form". Here
        # the form is saved if the case occures

        groups = Group.objects.filter(user=request.user, name__contains='extern').all()
        show_company_form = len(groups)

        unlinked_company_form = None
        if (show_company_form == 0):
            unlinked_company_form = CompanyForm(request.POST or None)

        if (unlinked_company_form is not None and unlinked_company_form.is_valid() and permit_form.is_valid()) \
            or (unlinked_company_form is  None and permit_form.is_valid()):

            # Gets the data before pushing it to database
            permitRequest = permit_form.save(commit=False)
            # Check for archeological zones from cantonal geodata
            has_archeo = archeo_checker(permit_form.cleaned_data['geom'])
            permit_form.instance.has_archeology = has_archeo

            # Add company
            if show_company_form == 0:
                new_company_actor = unlinked_company_form.save()
                permitRequest.company = new_company_actor
            else:
                permitRequest.company = Actor.objects.get(user=request.user)

            permitRequest.project_owner = Actor.objects.get(pk=project_owner_id)
            permitRequest.date_request_created = datetime.now()
            # Save it in database
            permitRequest.save()

            if has_archeo:
                permit_link = os.environ['PRODUCTION_ROOT_ADRESS'] + '/gpf/permitdetail/' + str(permitRequest.id)
                gpf.sendmail.send(permit_link, [], '', 'archeo_detected', '', permitRequest.administrative_entity)

            # Create empty validation objects related to this permit
            for dep in Department.objects.filter(is_validator=True, administrative_entity=permitRequest.administrative_entity).all():


                new_validation = Validation (
                    department=dep,
                    permitrequest=permitRequest,
                    accepted=False,
                    comment=''
                )

                new_validation.save()

            return HttpResponseRedirect(
                reverse('gpf:documentupload', args=(permitRequest.id,))
            )

    else:

        permit_form = AddPermitRequestForm()

        # if the request is filled by intern employees, the user ligin is not
        # linked to a company, thus, we add an "unlinked company form"

        groups = Group.objects.filter(user=request.user, name__contains='extern').all()
        show_company_form = len(groups)

        unlinked_company_form = CompanyForm(request.POST or None)


    return render(request, 'gpf/request_add.html',
        {'form': permit_form,
        'unlinked_company_form': unlinked_company_form,
        'show_company_form': show_company_form})


@permission_required('gpf.view_permitrequest')
def permitdetail(request, pk):

    instance = get_object_or_404(PermitRequest, pk=pk)
    form = ChangePermitRequestForm(request.POST or None, instance=instance)

    # enable/disable permitrequest fields depending on user permissions
    for field in form.fields:

        current_user_permission = not field_permission_checker(field, request.user, 'gpf.change')
        form.fields[field].disabled = current_user_permission

        if not current_user_permission:
            form.fields[field].widget.attrs['class'] = 'highlight-edit'

        # admin's backdoor
        if str(request.user) == 'admin':
            form.fields[field].disabled = False

    form.fields['geom'].widget.attrs['edit_geom'] = field_permission_checker('geom', request.user, 'gpf.change')
    # Allow final validation only if all validation are ok
    # form.fields['validated'].disabled = validation_checker(instance)
    form.fields['archeotype'].required = False

    ValidationFormSet = inlineformset_factory(
        PermitRequest,
        Validation,
        form=ValidationForm,
        fields=('accepted', 'comment',),
        extra=0,
        can_delete=False
    )

    validation_formset = ValidationFormSet(
        request.POST or None,
        instance=instance,
    )

    user = User.objects.get(id=request.user.id)
    query_set = Group.objects.filter(user = request.user)

    #enable/disable validations depending on user validator group
    validations = []
    num_validation = 0
    for dep in Department.objects.filter(is_validator=True, administrative_entity=instance.administrative_entity).all():
        print(num_validation)
        validations.append({
            'department': dep.id,
            'group_id': dep.group_id,
        })
        num_validation += 1
    i = 0
    for sform in validation_formset:
        valid = validations[i]
        group_name = Group.objects.filter(id=validations[i]['group_id'])[0]

        disable_validation = True
        for group in request.user.groups.all():
            if group_name == group:
                disable_validation = False
        i += 1
        for field in sform.fields:
            sform.fields[field].disabled = disable_validation
            if not disable_validation:
                sform.fields[field].widget.attrs['class'] = 'highlight-edit'
            if sform.fields[field].label:
                sform.fields[field].label += ' ' + group_name.department.description


    if form.is_valid():
        instance = form.save()
        for sform in validation_formset:
            if sform.is_valid():
                sform.save()

        # Save ok, return to home for intern users
        return HttpResponseRedirect(reverse('gpf:list'))

    documents = Document.objects.filter(permitrequest=pk).all()

    return render(request, 'gpf/edit.html', {
        'form': form,
        'validation_formset': validation_formset,
        'permit_id': pk,
        'documents': documents
    })


@login_required
def documentUpload(request, permit_id):

    if request.method == 'POST':

        form = DocumentForm(request.POST, request.FILES)
        template_name = 'gpf/upload.html'  # Replace with your template.

        if form.is_valid():

            files = request.FILES.getlist('file_path')
            permitrequest= PermitRequest.objects.get(pk=permit_id)
            for f in files:
                save_file_path = handle_uploaded_file(f)
                new_document = Document(
                    permitrequest=permitrequest,
                    file_path=save_file_path,
                    file_name=f.name
                )

                new_document.save()

            return HttpResponseRedirect(
                reverse('gpf:thanks', args=(permit_id,))
            )
    else:
        form = DocumentForm()

    return render(request, 'gpf/upload.html', {'form': form, 'permit_id': permit_id})



@permission_required('gpf.change_sent')
def sendpermit(request, pk):

    Thread(target=sendpermit_thread, args=(request, pk)).start()
    messagetxt = 'Le message de confirmation du permis n° ' + str(pk)
    messagetxt += ' vous parviendra d\'ici quelques minutes'
    messages.info(request, messagetxt)
    return HttpResponseRedirect(reverse('gpf:list'))


def sendpermit_thread(request, pk):

    permitrequest= PermitRequest.objects.get(pk=pk)
    pdf_file, permit_path = gpf.print.printreport(request, pk, True)
    permit_link = ''

    gpf.sendmail.send(
        permit_link,
        ['Directives_2017.pdf', 'Mode_refection_fouilles.pdf', 'Fin_des_travaux_form.pdf'],
        permit_path, 'permit_send', '',
        permitrequest.administrative_entity
    )


@permission_required('gpf.view_permitrequest')
def printpermit(request, pk):

    pdf_file, filepath = gpf.print.printreport(request, pk, True)
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="permis_fouille.pdf"'
    return response


@permission_required('gpf.change_sent')
def callforvalidations(request, pk):

    validation_remainder_mail(request, pk)
    messagetxt = 'La demande de validation aux services retardataires pour le permis n° '
    messagetxt +=  str(pk) + ' a été expédiée'
    messages.info(request, messagetxt)
    return HttpResponseRedirect(reverse('gpf:list'))


@permission_required('gpf.view_permitrequest')
def seewaitingvalidations(request, pk):

    groups = Group.objects.filter(department__validation__permitrequest__id=pk,
        department__validation__accepted=False).all()

    group_users = []

    all_validated = False

    if len(groups) == 0:

        all_validated = True

    else:

        for group in groups:

            users = User.objects.filter(groups__name=group.name)
            user_list = []
            for user in users:
                userdict = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                }
                user_list.append(userdict)

            group_users.append({
                'group_name': group.department.description,
                'user_details': user_list
            })

    return render(request, 'gpf/waitingvalidations.html', {
        'group_users': group_users,
        'permit_id': pk,
        'all_validated': all_validated
    })


@permission_required('gpf.change_sent')
def serviceusers(request):

    group_users = []
    #TODO: fitler for administrative_entity
    groups = Group.objects.filter(department__is_validator=True).all()

    for group in groups:

        users = User.objects.filter(groups__name=group.name)
        user_list = []
        for user in users:
            userdict = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
            user_list.append(userdict)

        group_users.append({
            'group_name': group.department.description,
            'user_details': user_list
        })

    return render(request, 'gpf/servicesusers.html', {
        'group_users': group_users,
    })


@permission_required('gpf.change_sent')
def waitingvalidations(request, hours):

    waiting_validations(request, hours)

    return HttpResponseRedirect(reverse('gpf:list'))


@permission_required('gpf.view_permitrequest')
def file_download (request, pk):
    document = Document.objects.get(pk=pk)
    response = FileResponse(open(document.file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + document.file_path
    return response


class PermitRequestDelete(PermissionRequiredMixin, DeleteView):
    model = PermitRequest
    success_url = "/gpf/list"
    permission_required = ('gpf.delete_permitrequest')


@login_required
def actorAdd(request):

    form = ActorForm(request.POST or None)

    if form.is_valid():
        new_actor = form.save()
        return HttpResponseRedirect(
            reverse('gpf:permit-request-add', args=(new_actor.id,)))
    return render(request, 'gpf/actor_form.html', {'form' : form})


@login_required
def companyedit(request, pk):

    instance = get_object_or_404(Actor, pk=pk)
    form = CompanyForm(request.POST or None, instance=instance)

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('gpf:listexterns'))
    else:
        form = CompanyForm(request.POST or None, instance=instance)

    return render(request, "gpf/company_change.html", {'form': form})


@login_required
def genericactorview(request, pk):

    instance = get_object_or_404(Actor, pk=pk)
    form = GenericActorForm(request.POST or None, instance=instance)

    for field in form.fields:

        form.fields[field].disabled = True

    return render(request, "gpf/genericactorview.html", {'form': form})


def companyAdd(request):

    signupform = companyUserAddForm(request.POST or None)

    form = CompanyForm(request.POST or None)

    if signupform.is_valid() and form.is_valid():

        signupform.instance.first_name = form.instance.firstname
        signupform.instance.last_name = form.instance.name
        signupform.instance.email = form.instance.email
        new_user = signupform.save()
        group = Group.objects.filter(name='extern').first()
        new_user.groups.add(group)
        form.instance.user = new_user
        new_company= form.save()

        login(request, new_user)

        return HttpResponseRedirect(
            reverse('gpf:listexterns'))

    return render(request, "gpf/company_form.html", {'form' : form, 'signupform': signupform})


@permission_required('gpf.can_change', raise_exception=True)
def actorChange(request, pk=None):
    instance = get_object_or_404(Actor, pk=pk)
    form = ActorForm(request.POST or None, instance=instance)

    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_actor");</script>' % \
            (instance.pk, instance))
    return render(request, "gpf/actor_form.html", {'form' : form})


@login_required
def actor_edit_account(request):

    user = Actor.objects.filter(user=request.user.pk).first()
    form = ActorForm(request.POST or None, instance=user)

    if form.is_valid():
        instance = form.save()

        if request.user.groups.filter(name = "extern").exists():
            return HttpResponseRedirect(reverse('gpf:listexterns'))
        else:
            return HttpResponseRedirect(reverse('gpf:list'))

    return render(request, "gpf/actor_edit_account.html", {'form' : form})


@login_required
def endwork(request, pk):

    instance = get_object_or_404(PermitRequest, pk=pk, company=Actor.objects.get(user__username=request.user))
    form = EndWorkForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.instance.date_end_work_announcement = datetime.now()
        instance = form.save()
        permit_link = os.environ['PRODUCTION_ROOT_ADRESS'] + '/gpf/permitdetail/' + str(pk)
        gpf.sendmail.send(permit_link, [], '',  'end_work_announcement', '', instance.administrative_entity)
        return HttpResponseRedirect(reverse('gpf:listexterns'))

    return render(request, "gpf/end_work.html", {'form' : form})


class PermitRequestListView(PermissionRequiredMixin, SingleTableMixin, FilterView):
    paginate_by = int(os.environ['PAGINATE_BY'])
    table_class = PermitRequestTable
    model = PermitRequest
    template_name = 'gpf/list.html'
    filterset_class = PermitRequestFilter
    permission_required = 'gpf.view_permitrequest'

    def get_queryset(self):

        groups = Group.objects.filter(user=self.request.user).all()
        administrative_entities = []

        if str(self.request.user) == 'admin':
            for adm in AdministrativeEntity.objects.all():
                administrative_entities.append(adm)

        else:

            for group in groups:

                if group.department.administrative_entity not in administrative_entities:
                    administrative_entities.append(group.department.administrative_entity)

        return PermitRequest.objects.filter(administrative_entity__in=administrative_entities)


@method_decorator(login_required, name="dispatch")
class PermitRequestListExternsView(SingleTableMixin, FilterView):

    paginate_by = int(os.environ['PAGINATE_BY'])
    table_class = PermitRequestTableExterns
    model = PermitRequest
    template_name = 'gpf/listexterns.html'
    filterset_class = PermitRequestFilterExterns

    def get_queryset(self):
        return PermitRequest.objects.filter(company=Actor.objects.get(user__username=self.request.user))


@method_decorator(login_required, name="dispatch")
class PermitExportView(PermissionRequiredMixin, ExportMixin, SingleTableView):
    table_class = PermitExportTable
    model = PermitRequest
    template_name = 'django_tables2/bootstrap.html'
    permission_required = ('gpf.view_permitrequest')
    exclude_columns = ("edit_entries", "print", "administrative", )


@method_decorator(login_required, name="dispatch")
class PermitExportViewExterns(ExportMixin, SingleTableView):
    table_class = PermitExportTable
    model = PermitRequest
    template_name = 'django_tables2/bootstrap.html'
    exclude_columns = ("edit_entries", "print", "administrative", )

    def get_queryset(self):
        return PermitRequest.objects.filter(company=Actor.objects.get(user__username=self.request.user))


@login_required
def thanks(request, permit_id):

    permitrequest= PermitRequest.objects.get(pk=permit_id)
    permit_link = os.environ['PRODUCTION_ROOT_ADRESS'] + '/gpf/permitdetail/' + str(permit_id)

    gpf.sendmail.send(
        permit_link, ['Directives_2017.pdf', 'Mode_refection_fouilles.pdf'],
        '',
        'permit_confirmation',
        [request.user.email],
        permitrequest.administrative_entity
    )
    gpf.sendmail.send(permit_link, [], '', 'new_permit', '', permitrequest.administrative_entity)

    return render(request, 'gpf/thanks.html')


@login_required
def prices(request):

    return render(request, 'gpf/prices.html')


@login_required
def mapnv(request, pk):

    permit = PermitRequest.objects.filter(pk=pk).first()
    extent = permit.geom.extent
    centerx = round((extent[0] + extent[2])/2)
    centery = round((extent[1] + extent[3])/2)
    gmf_base_url = os.environ['GMF_BASE_URL']
    target_url = gmf_base_url + "/theme/permis_fouille?"
    target_url += '&tree_groups=Permis%20de%20fouille&tree_group_layers_Permis%20de%20fouille=STE_gpf_demande'
    target_url += '&map_x=' + str(centerx) + '&map_y=' + str(centery) + '&map_zoom=5'

    return redirect(target_url)


@login_required
def adm_entity_geojson(request):

    geojson_geom = json.loads(serialize('geojson', AdministrativeEntity.objects.all(),
              geometry_field='geom',
              srid=2056,
              fields=('pk','name','ofs_id',)))

    return JsonResponse(geojson_geom, safe=False)
