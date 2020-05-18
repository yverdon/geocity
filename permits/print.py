import os, datetime
from weasyprint import HTML, CSS
from django.shortcuts import get_object_or_404, render
from django.conf import settings
import urllib.parse
import urllib.request
from uuid import uuid4
from . import services, models, forms


def get_permit_request_for_edition(user, permit_request_id):
    return services.get_permit_request_for_user_or_404(
        user,
        permit_request_id,
        statuses=[
            models.PermitRequest.STATUS_DRAFT,
            models.PermitRequest.STATUS_AWAITING_SUPPLEMENT
        ]
    )


def printreport(request, permit_request_id):

    permit_request = get_permit_request_for_edition(request.user, permit_request_id)

    print_date = datetime.datetime.now()

    properties_form = forms.WorksObjectsPropertiesForm(instance=permit_request)
    properties_by_object_type = dict(properties_form.get_fields_by_object_type())
    appendices_form = forms.WorksObjectsAppendicesForm(instance=permit_request)
    appendices_by_object_type = dict(appendices_form.get_fields_by_object_type())

    objects_infos = [
        (
            obj,
            properties_by_object_type.get(obj, []),
            appendices_by_object_type.get(obj, [])
        )
        for obj in permit_request.works_object_types.all()
    ]

    actor_types = dict(models.ACTOR_TYPE_CHOICES)

    contacts = [
        (actor_types.get(contact['actor_type'].value(), ''), [
            (field.label, field.value())
            for field in contact
            if field.name not in {'id', 'actor_type'}
        ])
        for contact in services.get_permitactorformset_initiated(permit_request)
        if contact['id'].value()
    ]


    html = render(request, "permits/print/printpermit.html", {
        'permit_request': permit_request,
        'contacts': contacts,
        'objects_infos': objects_infos,
    })

    pdf_file = HTML(string=html.content,  base_url=request.build_absolute_uri()).write_pdf(
        stylesheets=[CSS('/code/static/css/printpermit.css')]) #FIX THAT
    file_path = 'tutu'
    return pdf_file, file_path
