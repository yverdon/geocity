from django_cron import CronJobBase, Schedule
from datetime import date, datetime, timedelta
from .models import WorksObjectType, PermitRequest
from django.db.models import Max, Min
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from .services import send_email_notification


class PermitRequestExpirationReminder(CronJobBase):
    # If it runs once a day by a crontab, any value of less than 1440 is ok for the
    # RUN_EVERY_MINS variable, it just limits the execution of the script in case it
    # is called repeatedly.
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "permits.permit_request_expiration_reminder"

    def do(self):
        permit_requests_to_remind = (
            PermitRequest.objects.filter(works_object_types__expiration_reminder=True)
            .annotate(
                ends_at_max=Max("geo_time__ends_at"),
                reminder_delta=Max("works_object_types__days_before_reminder"),
            )
            .distinct()
        )

        for permit_request in permit_requests_to_remind:
            expiration_day = date.today() + timedelta(
                days=permit_request.reminder_delta
            )
            prolongation_date = (
                permit_request.prolongation_date.date()
                if permit_request.is_prolonged()
                else None
            )

            if expiration_day in [permit_request.ends_at_max.date(), prolongation_date]:
                data = {
                    "subject": _("Votre autorisation #%s arrive bientôt à échéance")
                    % permit_request.id,
                    "users_to_notify": [permit_request.author.user.email],
                    "template": "permit_request_prolongation_reminder.txt",
                    "permit_request": permit_request,
                    "absolute_uri_func": None,
                }
                send_email_notification(data)

        print("Cron Ran")
