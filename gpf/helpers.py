from .models import Validation, Department, Archelogy, PermitRequest
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta
import gpf.sendmail
import os
from uuid import uuid4 as uuid

#check if user has permission for given field
def field_permission_checker(field, user, right_def):

    user_permissions = user.get_all_permissions()
    field_permission = right_def + '_' + field
    if field_permission in user_permissions:
        return True
    else:
        return False


#check if all validations are done for permit
def validation_checker(permit):

    validated = Validation.objects.filter(permitrequest=permit.id, accepted=True).count()
    validators = Department.objects.filter(is_validator=True).count()

    if validated < validators:
        return True
    else:
        return False


#send mail to department who did not validate the permit
def validation_remainder_mail(request, pk):

    groups = Group.objects.filter(department__validation__permitrequest__id=pk,
        department__validation__accepted=False).all()

    users = User.objects.filter(groups__in=groups).exclude(username='admin').all().values('email')

    recipients = []
    for mail in users:
        recipients.append(mail['email'])

    permit_link = os.environ['PRODUCTION_ROOT_ADRESS'] + '/gpf/permitdetail/' + str(pk)

    gpf.sendmail.send(permit_link, [], '',  'single_validation_remainder', recipients)


#send mails to all services that are late on the validation process
def waiting_validations(request, hours):

    past = datetime.now() - timedelta(hours=hours)
    # permits that are older that x hours but not validated yet
    permits = PermitRequest.objects.filter(validated=False, date_request_created__lt=past).all()
    #validation that belong to the permits above but are nor accepted yet
    waiting_validations = Validation.objects.filter(permitrequest__in=permits, accepted=False)
    #groups corresponding to waiting validations

    # list_mails = []
    for validation in waiting_validations:
        groups = Group.objects.filter(department__validation=validation).all()
        users = User.objects.filter(groups__in=groups).exclude(username='admin').all().values('email')
        permit_link = os.environ['PRODUCTION_ROOT_ADRESS'] + '/gpf/permitdetail/' + str(validation.permitrequest.id)
        recipients = list(users.values_list('email', flat=True))

        if len(recipients) > 0:
            gpf.sendmail.send(permit_link, [], '',  'daily_validation_remainder', recipients)


# write uploaded file to disk
def handle_uploaded_file(f):

    file_path_on_disk = os.environ["DOCUMENT_FOLDER"] + '/uploads/' + str(uuid()) + '_' + f.name

    with open(file_path_on_disk, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return file_path_on_disk


#check for the presence of archeology
def archeo_checker(geom):
    archeo_polygons= Archelogy.objects.filter(geom__intersects=geom.buffer(10))
    archeo_polygons_eca = []
    for polygon in archeo_polygons:
        archeo_polygons_eca.append(polygon.eca)

    has_archeology = False

    if len(archeo_polygons_eca) > 0:
        has_archeology = True


    return has_archeology
