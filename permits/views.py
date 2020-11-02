import logging
import mimetypes
import urllib.parse
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.exceptions import SuspiciousOperation
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from django.views import View
from django_tables2.views import SingleTableMixin, SingleTableView
from django_tables2.export.views import ExportMixin
from django_filters.views import FilterView
from . import fields, forms, models, services, tables, filters, printpermit
from django.utils import timezone
from django.http import Http404, HttpResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required


from .exceptions import BadPermitRequestStatus


logger = logging.getLogger(__name__)


def user_has_permitauthor(user):
    try:
        user.permitauthor
    except models.PermitAuthor.DoesNotExist:
        return False

    return True


def get_permit_request_for_edition(user, permit_request_id):
    return services.get_permit_request_for_user_or_404(
        user,
        permit_request_id,
        statuses=[
            models.PermitRequest.STATUS_DRAFT,
            models.PermitRequest.STATUS_AWAITING_SUPPLEMENT
        ]
    )


def redirect_bad_status_to_detail(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BadPermitRequestStatus as e:
            return redirect('permits:permit_request_detail', permit_request_id=e.permit_request.pk)

    return inner


def disable_form(form):
    for field in form.fields.values():
        field.disabled = True

    form.disabled = True

    return form


@method_decorator(login_required, name='dispatch')
class PermitRequestDetailView(View):
    ACTION_AMEND = "amend"
    ACTION_REQUEST_VALIDATION = "request_validation"
    ACTION_VALIDATE = "validate"
    ACTION_POKE = "poke"

    # If you add an action here, make sure you also handle it in `get_form_for_action` and in `handle_form_submission`
    actions = [ACTION_AMEND, ACTION_REQUEST_VALIDATION, ACTION_VALIDATE, ACTION_POKE]

    def dispatch(self, request, *args, **kwargs):
        self.permit_request = services.get_permit_request_for_user_or_404(
            request.user, kwargs["permit_request_id"])

        if self.permit_request.is_draft() and self.permit_request.author.user == request.user:
            return redirect(
                'permits:permit_request_select_administrative_entity', permit_request_id=self.permit_request.pk
            )

        return super().dispatch(request, *args, **kwargs)

    def render_to_response(self, context):
        return render(self.request, "permits/permit_request_detail.html", context)

    def get_context_data(self, **kwargs):

        current_actions = services.get_actions_for_administrative_entity(self.actions,
                                                                         self.permit_request.administrative_entity)

        forms = {action: self.get_form_for_action(action) for action in current_actions}
        available_actions = [action for action in current_actions if forms[action]]

        try:
            active_form = [
                action for action in available_actions if not getattr(forms[action], "disabled", False)
            ][0]
        except IndexError:
            active_form = available_actions[-1] if len(available_actions) > 0 else None

        kwargs["has_validations"] = self.permit_request.has_validations()

        if forms.get(self.ACTION_POKE):
            kwargs["nb_pending_validations"] = self.permit_request.get_pending_validations().count()
            kwargs["validations"] = self.permit_request.validations.select_related(
                "department", "department__group")
        else:
            kwargs["nb_pending_validations"] = 0

            if services.can_validate_permit_request(self.request.user, self.permit_request):
                kwargs["validations"] = self.permit_request.validations.select_related(
                    "department", "department__group")
            else:
                kwargs["validations"] = []

        return {**kwargs, **{
            "permit_request": self.permit_request,
            "forms": forms,
            "active_form": active_form,
            "has_permission_to_classify": services.has_permission_to_classify_permit_request(
                self.request.user, self.permit_request
            ),
            "can_classify": services.can_classify_permit_request(self.request.user, self.permit_request),
        }}

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Instanciate the form matching the submitted POST `action`, checking if the user has the permissions to use it,
        save it, and call the related submission function.
        """

        action = request.POST.get("action")

        if action not in self.actions:
            return HttpResponse(status=400)

        form = self.get_form_for_action(action, data=request.POST)

        if not form:
            raise PermissionDenied
        elif getattr(form, "disabled", False):
            raise SuspiciousOperation

        if form.is_valid():
            return self.handle_form_submission(form, action)

        # Replace unbound form by bound form in the context
        context = self.get_context_data()
        context["forms"][action] = form

        return self.render_to_response(context)

    def get_form_for_action(self, action, data=None):
        actions_forms = {
            self.ACTION_AMEND: self.get_amend_form,
            self.ACTION_REQUEST_VALIDATION: self.get_request_validation_form,
            self.ACTION_VALIDATE: self.get_validation_form,
            self.ACTION_POKE: self.get_poke_form,
        }

        return actions_forms[action](data=data)

    def get_amend_form(self, data=None):

        if services.has_permission_to_amend_permit_request(self.request.user, self.permit_request):
            # Only set the `status` default value if it's submitted for validation, to prevent accidentally resetting
            # the status
            initial = {
                "status": models.PermitRequest.STATUS_PROCESSING
            } if self.permit_request.status == models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION else {}

            form = forms.PermitRequestAdditionalInformationForm(
                instance=self.permit_request, initial=initial, data=data
            )

            if not services.can_amend_permit_request(self.request.user, self.permit_request):
                disable_form(form)

            return form

        return None

    def get_request_validation_form(self, data=None):
        if services.has_permission_to_amend_permit_request(self.request.user, self.permit_request):
            form = forms.PermitRequestValidationDepartmentSelectionForm(
                instance=self.permit_request, data=data)

            if not services.can_amend_permit_request(self.request.user, self.permit_request):
                disable_form(form)

            return form

        return None

    def get_validation_form(self, data=None):
        if not services.has_permission_to_validate_permit_request(self.request.user, self.permit_request):
            return None

        departments = services.get_user_departments(self.request.user)

        try:
            validation, *rest = list(
                self.permit_request.validations.filter(department__in=departments)
            )
        # User is not part of the requested departments
        except ValueError:
            return None

        if rest:
            logger.error(
                "User %s is a member of more than 1 validation group for permit request %s. This is not"
                " implemented yet.", self.request.user, self.permit_request
            )
            return None

        form = forms.PermitRequestValidationForm(instance=validation, data=data)

        if not services.can_validate_permit_request(self.request.user, self.permit_request):
            disable_form(form)

        return form

    def get_poke_form(self, data=None):
        if services.has_permission_to_poke_permit_request(self.request.user, self.permit_request):
            form = forms.PermitRequestValidationPokeForm(
                instance=self.permit_request, request=self.request, data=data)
            if not services.can_poke_permit_request(self.request.user, self.permit_request):
                disable_form(form)

            return form

        return None

    def handle_form_submission(self, form, action):
        if action == self.ACTION_AMEND:
            return self.handle_amend_form_submission(form)
        elif action == self.ACTION_REQUEST_VALIDATION:
            return self.handle_request_validation_form_submission(form)
        elif action == self.ACTION_VALIDATE:
            return self.handle_validation_form_submission(form)
        elif action == self.ACTION_POKE:
            return self.handle_poke(form)

    def handle_amend_form_submission(self, form):

        form.save()
        success_message = _(
            "La demande de permis #%s a bien été complétée par le service pilote.") % self.permit_request.pk

        if form.instance.status == models.PermitRequest.STATUS_AWAITING_SUPPLEMENT:
            success_message += " " + _(
                "Le statut de la demande a été passé à en attente de compléments. Vous devez maintenant"
                " contacter le requérant par email (%s) afin de lui demander de fournir les informations manquantes."
            ) % self.permit_request.author.user.email

        messages.success(self.request, success_message)

        return redirect("permits:permit_requests_list")

    def handle_request_validation_form_submission(self, form):
        services.request_permit_request_validation(
            self.permit_request, form.cleaned_data["departments"], self.request.build_absolute_uri
        )
        messages.success(
            self.request, _(
                "La demande de permis #%s a bien été transmise pour validation.") % self.permit_request.pk
        )
        return redirect("permits:permit_requests_list")

    def handle_validation_form_submission(self, form):

        form.instance.validated_at = timezone.now()
        form.instance.validated_by = self.request.user
        validation = form.save()

        if validation.validation_status == models.PermitRequestValidation.STATUS_APPROVED:
            validation_message = _("La demande a bien été validée.")
        elif validation.validation_status == models.PermitRequestValidation.STATUS_REJECTED:
            validation_message = _("La demande a bien été refusée.")
        else:
            validation_message = _("Les commentaires ont été enregistrés.")

        messages.success(self.request, validation_message)

        return redirect("permits:permit_requests_list")

    def handle_poke(self, form):
        validations = form.save()

        message = ngettext(
            "%s rappel a bien été envoyé.", "%s rappels ont bien été envoyés", len(validations)
        ) % (len(validations))
        messages.success(self.request, message)

        return redirect("permits:permit_requests_list")


@redirect_bad_status_to_detail
@login_required
@user_passes_test(user_has_permitauthor)
def permit_request_select_administrative_entity(request, permit_request_id=None):
    if permit_request_id:
        permit_request = get_permit_request_for_edition(request.user, permit_request_id)
    else:
        permit_request = None

    if request.method == 'POST':
        administrative_entity_form = forms.AdministrativeEntityForm(
            instance=permit_request, data=request.POST
        )

        if administrative_entity_form.is_valid():
            permit_request = administrative_entity_form.save(author=request.user.permitauthor)

            return redirect(
                reverse('permits:permit_request_select_types', kwargs={
                        'permit_request_id': permit_request.pk})
            )
    else:
        administrative_entity_form = forms.AdministrativeEntityForm(instance=permit_request)

    return render(request, "permits/permit_request_select_administrative_entity.html", {
        'form': administrative_entity_form,
        'permit_request': permit_request,
    })


@redirect_bad_status_to_detail
@login_required
def permit_request_select_types(request, permit_request_id):
    """
    Step to select works types (eg. demolition). No permit request is created at this step since we only store (works
    object, works type) couples in the database.
    """
    permit_request = get_permit_request_for_edition(request.user, permit_request_id)

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


@redirect_bad_status_to_detail
@login_required
def permit_request_select_objects(request, permit_request_id):
    """
    Step to select works objects. This view supports either editing an existing permit request (if `permit_request_id`
    is set) or creating a new permit request.
    """
    permit_request = get_permit_request_for_edition(request.user, permit_request_id)

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
    works_types = works_types.union(
        services.get_permit_request_works_types(permit_request)).distinct()

    if request.method == 'POST':
        works_objects_form = forms.WorksObjectsForm(
            data=request.POST, instance=permit_request, works_types=works_types
        )

        if works_objects_form.is_valid():
            permit_request = works_objects_form.save()
            return redirect('permits:permit_request_properties', permit_request_id=permit_request.pk)
    else:
        works_objects_form = forms.WorksObjectsForm(
            instance=permit_request, works_types=works_types)

    return render(request, "permits/permit_request_select_objects.html", {
        'works_objects_form': works_objects_form,
        'permit_request': permit_request
    })


@redirect_bad_status_to_detail
@login_required
def permit_request_properties(request, permit_request_id):
    """
    Step to input properties values for the given permit request.
    """
    permit_request = get_permit_request_for_edition(request.user, permit_request_id)

    if request.method == 'POST':
        # Disable `required` fields validation to allow partial save
        form = forms.WorksObjectsPropertiesForm(
            instance=permit_request, data=request.POST, enable_required=False)

        if form.is_valid():
            form.save()
            return redirect('permits:permit_request_geo_time', permit_request_id=permit_request.pk)
    else:
        form = forms.WorksObjectsPropertiesForm(instance=permit_request, enable_required=False)

    fields_by_object_type = form.get_fields_by_object_type()

    return render(request, "permits/permit_request_properties.html", {
        'permit_request': permit_request,
        'object_types': fields_by_object_type,
    })


@redirect_bad_status_to_detail
@login_required
def permit_request_appendices(request, permit_request_id):
    """
    Step to upload appendices for the given permit request.
    """
    permit_request = get_permit_request_for_edition(request.user, permit_request_id)

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


@redirect_bad_status_to_detail
@login_required
def permit_request_actors(request, permit_request_id):
    permit_request = get_permit_request_for_edition(request.user, permit_request_id)

    creditorform = forms.PermitRequestCreditorForm(request.POST or None, instance=permit_request)

    if request.method == 'POST':
        formset = services.get_permitactorformset_initiated(permit_request, data=request.POST)
        if formset.is_valid() and creditorform.is_valid():
            for form in formset:
                form.save(permit_request=permit_request)

            models.PermitRequest.objects.filter(
                pk=permit_request_id
            ).update(creditor_type=creditorform.instance.creditor_type)

            return redirect('permits:permit_request_submit', permit_request_id=permit_request.pk)
    else:

        formset = services.get_permitactorformset_initiated(permit_request)

    return render(request, "permits/permit_request_actors.html", {
        'formset': formset,
        'creditorform': creditorform,
        'permit_request': permit_request,
    })


@login_required
def permit_request_geo_time(request, permit_request_id):

    permit_request = services.get_permit_request_for_user_or_404(request.user, permit_request_id)

    instance = permit_request.geo_time.first()

    form = forms.PermitRequestGeoTimeForm(
        request.POST or None, instance=instance, permit_request=permit_request)

    if request.method == 'POST':

        if form.is_valid():
            form.instance.permit_request = permit_request
            form.save()

            return redirect('permits:permit_request_appendices', permit_request_id=permit_request_id)

    return render(request, "permits/permit_request_geo_time.html", {
        'form': form,
        'permit_request': permit_request,
    })


@login_required
def permit_request_media_download(request, property_value_id):
    """
    Send the file referenced by the given property value.
    """
    property_value = get_object_or_404(
        models.WorksObjectPropertyValue.objects.filter(
            property__input_type=models.WorksObjectProperty.INPUT_TYPE_FILE),
        pk=property_value_id,
        works_object_type_choice__permit_request__in=services.get_permit_requests_list_for_user(
            request.user)
    )
    file = services.get_property_value(property_value)
    mime_type, encoding = mimetypes.guess_type(file.name)

    return StreamingHttpResponse(file, content_type=mime_type)


@method_decorator(login_required, name="dispatch")
class PermitRequestList(SingleTableMixin, FilterView):
    paginate_by = int(os.environ['PAGINATE_BY'])
    template_name = 'permits/permit_requests_list.html'

    def get_queryset(self):
        return services.get_permit_requests_list_for_user(self.request.user).prefetch_related(
            Prefetch(
                'works_object_types',
                queryset=models.WorksObjectType.objects.select_related('works_type', 'works_object')
            )
        ).order_by('-created_at')

    def is_department_user(self):
        return self.request.user.groups.filter(permitdepartment__isnull=False).exists()

    def get_table_class(self):
        return (
            tables.DepartmentPermitRequestsTable
            if self.is_department_user()
            else tables.OwnPermitRequestsTable
        )

    def get_filterset_class(self):
        return (
            filters.DepartmentPermitRequestFilterSet
            if self.is_department_user()
            else filters.OwnPermitRequestFilterSet
        )


@method_decorator(login_required, name="dispatch")
class PermitExportView(ExportMixin, SingleTableView):
    table_class = tables.OwnPermitRequestsTable
    template_name = 'django_tables2/bootstrap.html'

    def get_queryset(self):
        return services.get_permit_requests_list_for_user(self.request.user).prefetch_related(
            Prefetch(
                'works_object_types',
                queryset=models.WorksObjectType.objects.select_related('works_type', 'works_object')
            )
        ).order_by('-created_at')
    exclude_columns = ("actions", )


@redirect_bad_status_to_detail
@login_required
def permit_request_submit(request, permit_request_id):

    permit_request = get_permit_request_for_edition(request.user, permit_request_id)

    incomplete_steps = [
        step.url
        for step in services.get_progressbar_steps(request, permit_request).values()
        if step.errors_count and step.url
    ]

    if request.method == 'POST':
        if incomplete_steps:
            raise SuspiciousOperation

        services.submit_permit_request(permit_request, request.build_absolute_uri)
        return redirect('permits:permit_requests_list')

    return render(request, "permits/permit_request_submit.html", {
        'permit_request': permit_request,
        'incomplete_steps': incomplete_steps,
    })


@redirect_bad_status_to_detail
@login_required
def permit_request_submit_confirmation(request, permit_request_id):

    permit_request = get_permit_request_for_edition(request.user, permit_request_id)

    incomplete_steps = [
        step.url
        for step in services.get_progressbar_steps(request, permit_request).values()
        if step.errors_count and step.url
    ]

    if request.method == 'POST':
        if incomplete_steps:
            raise SuspiciousOperation

        services.submit_permit_request(permit_request, request.build_absolute_uri)
        return redirect('permits:permit_requests_list')

    return render(request, "permits/permit_request_send_confirmation.html", {
        'permit_request': get_permit_request_for_edition(request.user, permit_request_id)
    })


@redirect_bad_status_to_detail
@login_required
def permit_request_submit_confirmed(request, permit_request_id):

    permit_request = get_permit_request_for_edition(request.user, permit_request_id)

    incomplete_steps = [
        step.url
        for step in services.get_progressbar_steps(request, permit_request).values()
        if step.errors_count and step.url
    ]

    if incomplete_steps:
        raise SuspiciousOperation

    services.submit_permit_request(permit_request, request.build_absolute_uri)
    return redirect('permits:permit_requests_list')


@redirect_bad_status_to_detail
@login_required
def permit_request_delete(request, permit_request_id):
    permit_request = get_permit_request_for_edition(request.user, permit_request_id)

    if request.method == 'POST':
        permit_request.delete()

        return redirect('permits:permit_requests_list')

    return render(request, "permits/permit_request_delete.html", {
        'permit_request': permit_request
    })


def permit_request_approve(request, permit_request_id):
    return permit_request_classify(request, permit_request_id, approve=True)


def permit_request_reject(request, permit_request_id):
    return permit_request_classify(request, permit_request_id, approve=False)


@login_required
@permission_required("permits.classify_permit_request")
def permit_request_classify(request, permit_request_id, approve):
    permit_request = services.get_permit_request_for_user_or_404(
        request.user,
        permit_request_id,
        statuses=[
            models.PermitRequest.STATUS_AWAITING_VALIDATION,
            models.PermitRequest.STATUS_PROCESSING,
        ]
    )
    if not services.can_classify_permit_request(request.user, permit_request):
        raise Http404

    initial = {
        "status": (
            models.PermitRequest.STATUS_APPROVED
            if approve
            else models.PermitRequest.STATUS_REJECTED
        )
    }
    title = (_("Approbation de la demande #%s") if approve else _(
        "Refus de la demande #%s")) % permit_request.pk

    if request.method == "POST":
        classify_form = forms.PermitRequestClassifyForm(
            instance=permit_request, data=request.POST, files=request.FILES, initial=initial
        )

        if classify_form.is_valid():
            classify_form.save()
            return redirect("permits:permit_requests_list")
    else:
        classify_form = forms.PermitRequestClassifyForm(instance=permit_request, initial=initial)

    return render(request, "permits/permit_request_classify.html", {
        "permit_request": permit_request,
        "approve": approve,
        "form": classify_form,
        "title": title,
    })


def permit_request_file_download(request, path):
    """
    Securely download the permit request file at the given `path`. The path must start with the permit request id, such
    as returned by the `PermitRequestFieldFile`.

    If the user doesn't have access to the permit request identified by the given id, return an HTTP 404 error.
    """
    try:
        permit_request_id, _ = path.split("/", maxsplit=1)
    except ValueError:
        raise Http404

    services.get_permit_request_for_user_or_404(request.user, permit_request_id)

    mime_type, encoding = mimetypes.guess_type(path)
    storage = fields.PrivateFileSystemStorage()

    return StreamingHttpResponse(storage.open(path), content_type=mime_type)


@login_required
def administrative_entity_file_download(request, path):
    """
    Securely download the administrative entity customization files for member of the administrative_entity concerned
    """

    if services.get_user_administrative_entities(request.user).count() == 0 and not request.user.is_superuser:
        raise Http404

    mime_type, encoding = mimetypes.guess_type(path)
    storage = fields.PrivateFileSystemStorage()

    return StreamingHttpResponse(storage.open(path), content_type=mime_type)


@login_required
def printpdf(request, permit_request_id):

    permit_request = models.PermitRequest.objects.get(pk=permit_request_id)
    if request.user.has_perm('permits.amend_permit_request') and \
        (permit_request.has_validations() and
            permit_request.get_pending_validations().count() == 0) \
            or permit_request.status == 2:

        pdf_file = printpermit.printreport(request, permit_request)
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="permis.pdf"'
        return response
    else:
        raise PermissionDenied


@login_required
def genericauthorview(request, pk):

    instance = get_object_or_404(models.PermitAuthor, pk=pk)
    form = forms.GenericAuthorForm(request.POST or None, instance=instance)

    for field in form.fields:

        form.fields[field].disabled = True

    return render(request, "permits/permit_request_author.html", {'form': form})


@login_required
def administrative_infos(request):

    administrative_entities = models.PermitAdministrativeEntity.objects.all()

    return render(request, "permits/administrative_infos.html",
                           {'administrative_entities': administrative_entities})
