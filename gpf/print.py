import os, datetime
from .models import Validation, PermitRequest
from .forms import ChangePermitRequestForm,ActorForm
from weasyprint import HTML, CSS
from django.shortcuts import get_object_or_404, render
from django.conf import settings
import urllib.parse
import urllib.request
from uuid import uuid4
import base64

def printreport(request, pk, save_to_file):

    permit = get_object_or_404(PermitRequest, pk=pk)
    validations = Validation.objects.filter(permitrequest=pk)

    form_permit = ChangePermitRequestForm(request.POST or None, instance=permit)
    form_actor = ActorForm(request.POST or None, instance=permit.project_owner)
    print_date = datetime.datetime.now()

    # TODO: configure this from env.yaml file
    buffer_extent = os.environ["PRINT_MAP_BUFFER_METERS"]
    extent_raw = permit.geom.buffer(int(buffer_extent)).extent
    h_extent = extent_raw[2] - extent_raw[0]
    h_extent_center = h_extent/2 + extent_raw[0]
    h_extent_left =  round(extent_raw[0])
    h_extent_right =  round(extent_raw[2])
    v_extent_scaled = (extent_raw[3] - extent_raw[1]) * (1800/2500)
    v_extent_bottom = round(v_extent_scaled/2 + extent_raw[1])
    v_extent_top = round(v_extent_scaled + v_extent_bottom)

    extent = [h_extent_left, v_extent_bottom, h_extent_right, v_extent_top]

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
          'LAYERS' : 'basemaps,gpf_archelogy,ele_rohr,was_leitung,cad_leitung,awk_haltung,gas_leitung,gpf_permitrequest',
          'FILTER' : 'gpf_permitrequest:"id" >= ' +  str(permit.id) +' AND "id" < ' + str(permit.id + 1),
          }

    data = urllib.parse.urlencode(values)
    printurl = settings.QGISSERVER_URL + '/?' + data

    image_uuid = str(uuid4())
    map_image_name = 'permis_fouille_numero_' + str(pk) + '-' + image_uuid + '.png'
    image_path = settings.TEMPFILES_FOLDER + '/' + map_image_name
    map_request = urllib.request.urlretrieve(printurl, image_path)

    with open(image_path, "rb") as img_file:
        base64image = base64.b64encode(img_file.read()).decode("utf-8")

    with open(settings.YLB_PROTECTED_SIGNATURE, "rb") as signature_file:
        base64imagesignature = base64.b64encode(signature_file.read()).decode("utf-8")

    html = render(request, 'gpf/print/edit.html', {
        'form_permit': form_permit,
        'form_actor': form_actor,
        'permit_id': pk,
        'permit': permit,
        'validations': validations,
        'print_date': print_date,
        'base64imagestr': base64image,
        'base64imagesignaturestr': base64imagesignature,
        'root_url': os.environ['PRODUCTION_ROOT_ADRESS']
    })

    pdf_file = HTML(string=html.content,  base_url=request.build_absolute_uri()).write_pdf(
        stylesheets=[CSS(settings.STATIC_ROOT  +  '/css/print.css')])

    file_path = ''

    if save_to_file:
            file_name = 'permis_fouille_numero_' + str(pk) + '.pdf'
            file_path = os.environ["PRINTED_REPORT_FOLDER"] + '/' + \
                file_name
            with open(file_path, 'wb+') as destination:
                destination.write(pdf_file)
            permit = PermitRequest.objects.get(pk=pk)
            permit.report_filename = file_name
            permit.date_last_printed = datetime.datetime.now()
            permit.save()

    os.remove(image_path)
    return pdf_file, file_path
