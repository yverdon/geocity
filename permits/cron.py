import logging
from datetime import date, datetime, timedelta

from django.core.management import CommandError, call_command
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from django_cron import CronJobBase, Schedule

from .models import PermitRequest, PermitRequestInquiry
from .services import send_email_notification

logger = logging.getLogger(__name__)


class PermitRequestExpirationReminder(CronJobBase):
    RUN_AT_TIMES = ["23:30"]
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
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
            if permit_request.can_be_prolonged():
                expiration_day = date.today() + timedelta(
                    days=permit_request.reminder_delta
                )
                prolongation_date = (
                    permit_request.prolongation_date.date()
                    if permit_request.is_prolonged()
                    else None
                )

                if expiration_day in [
                    permit_request.ends_at_max.date(),
                    prolongation_date,
                ]:
                    data = {
                        "subject": _("Votre autorisation #%s arrive bientôt à échéance")
                        % permit_request.id,
                        "users_to_notify": [permit_request.author.user.email],
                        "template": "permit_request_prolongation_reminder.txt",
                        "permit_request": permit_request,
                        "absolute_uri_func": PermitRequest.get_absolute_url,
                    }
                    send_email_notification(data, None)

        logger.info("The permit expiration reminder Cronjob finished successfully")


class CleanupAnonymousRequests(CronJobBase):
    RUN_AT_TIMES = ["00:00"]
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = "permits.anonymous_permit_request_cleanup"

    def do(self):
        try:
            call_command("cleanup_anonymous_requests")
        except CommandError:
            logger.error(
                "Error occured while trying to cleanup the anonymous permit "
                "requests from the Cronjob."
            )
        else:
            logger.info(
                "The anonymous permit requests cleanup Cronjob finished successfully"
            )


class PermitRequestInquiryClosing(CronJobBase):
    RUN_AT_TIMES = ["15:00"]
    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = "permits.permit_request_inquiry_closing"

    def do(self):
        inquiries_to_close = PermitRequestInquiry.objects.filter(
            end_date=datetime.today().strftime("%Y-%m-%d")
        )

        for inquiry in inquiries_to_close:
            if (
                not inquiry.permit_request.status
                == PermitRequest.STATUS_INQUIRY_IN_PROGRESS
            ):
                continue

            inquiry.permit_request.status = PermitRequest.STATUS_PROCESSING
            inquiry.permit_request.save()

            data = {
                "subject": _("Fin de l'enquête publique"),
                "users_to_notify": [
                    inquiry.permit_request.author.user.email,
                    inquiry.submitter.email,
                ],
                "permit_request": inquiry.permit_request,
                "absolute_uri_func": inquiry.permit_request.get_absolute_url,
                "template": "permit_request_inquiry_closing.txt",
            }
            send_email_notification(data, None)

        logger.info("The permit inquiry closing Cronjob finished")


class PermitRequestInquiryOpening(CronJobBase):
    RUN_AT_TIMES = ["01:00"]
    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = "permits.permit_request_inquiry_opening"

    def do(self):
        inquiries_to_open = PermitRequestInquiry.objects.filter(
            start_date=datetime.today().strftime("%Y-%m-%d")
        )
        for inquiry in inquiries_to_open:
            if not inquiry.permit_request.status == PermitRequest.STATUS_PROCESSING:
                continue

            inquiry.permit_request.status = PermitRequest.STATUS_INQUIRY_IN_PROGRESS
            inquiry.permit_request.save()

        logger.info("The permit inquiry opening Cronjob finished")
