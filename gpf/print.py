import os, datetime
from .models import Validation, PermitRequest
from .forms import ChangePermitRequestForm,ActorForm
from weasyprint import HTML, CSS
from django.shortcuts import get_object_or_404, render
from django.conf import settings
import urllib.parse
import urllib.request
from uuid import uuid4

def printreport(request, pk, save_to_file):

    permit = get_object_or_404(PermitRequest, pk=pk)
    validations = Validation.objects.filter(permitrequest=pk)

    form_permit = ChangePermitRequestForm(request.POST or None, instance=permit)
    form_actor = ActorForm(request.POST or None, instance=permit.project_owner)
    print_date = datetime.datetime.now()

    extent_raw = permit.geom.buffer(200).extent
    extent = []

    for coord in extent_raw:
        extent.append(round(coord))

    url = settings.QGISSERVER_URL
    values = {'SERVICE' : 'WMS',
          'VERSION' : '1.3.0',
          'REQUEST' : 'GetPrint',
          'FORMAT' : 'png',
          'TRANSPARENT' : 'true',
          'SRS' : 'EPSG:2056',
          'DPI' : '150',
          'TEMPLATE' : 'permis-fouilles',
          'map0:extent' : ', '.join(map(str, extent)),
          'LAYERS' : 'gpf_permitrequest,basemaps',
          'FILTER' : 'gpf_permitrequest:"id" >= ' +  str(permit.id) +' AND "id" < ' + str(permit.id + 1),
          }

    data = urllib.parse.urlencode(values)
    printurl = settings.QGISSERVER_URL + '/?' + data

    map_image_path = ''

    image_uuid = str(uuid4())
    map_image_name = 'permis_fouille_numero_' + str(pk) + '-' + image_uuid + '.png'
    image_path = os.environ["TEMPFILES_FOLDER"] + '/' + map_image_name
    map_request = urllib.request.urlretrieve(printurl, image_path)
    print_image_url = os.environ["PRODUCTION_ROOT_ADRESS"] + "static/tempfiles/" + map_image_name

    html = render(request, 'gpf/print/edit.html', {
        'form_permit': form_permit,
        'form_actor': form_actor,
        'permit_id': pk,
        'permit': permit,
        'validations': validations,
        'print_date': print_date,
        'print_image_path': print_image_url,
        'root_url': os.environ['PRODUCTION_ROOT_ADRESS']
    })

    pdf_file = HTML(string=html.content,  base_url=request.build_absolute_uri()).write_pdf(
        stylesheets=[CSS(settings.STATIC_ROOT  +  '/css/print.css')])

    file_path = ''

    if save_to_file:
            file_name = 'permis_fouille_numero_' + str(pk) + '.pdf'
            file_path = os.environ["DOCUMENT_FOLDER"] + '/printed_reports/' + \
                file_name
            with open(file_path, 'wb+') as destination:
                destination.write(pdf_file)
            permit = PermitRequest.objects.get(pk=pk)
            permit.report_filename = file_name
            permit.date_last_printed = datetime.datetime.now()
            permit.save()

    os.remove(image_path)
    return pdf_file, file_path
