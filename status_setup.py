from permits import models

for status_value in models.PermitRequest.STATUS_CHOICES:
        for entity in models.PermitAdministrativeEntity.objects.all():
            models.PermitWorkFlowStatus.objects.get_or_create(
                status=status_value[0],
                administrative_entity=entity)
