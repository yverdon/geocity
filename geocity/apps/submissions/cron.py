import logging
from datetime import date, datetime, timedelta

from django.core.management import CommandError, call_command
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from django_cron import CronJobBase, Schedule

from .models import Submission, SubmissionInquiry
from .services import send_email_notification

logger = logging.getLogger(__name__)


class SubmissionExpirationReminder(CronJobBase):
    RUN_AT_TIMES = ["23:30"]
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = "submissions.submission_expiration_reminder"

    def do(self):
        submissions_to_remind = (
            Submission.objects.filter(works_object_types__expiration_reminder=True)
            .annotate(
                ends_at_max=Max("geo_time__ends_at"),
                reminder_delta=Max("forms__days_before_reminder"),
            )
            .distinct()
        )

        for submission in submissions_to_remind:
            if submission.can_be_prolonged():
                expiration_day = date.today() + timedelta(
                    days=submission.reminder_delta
                )
                prolongation_date = (
                    submission.prolongation_date.date()
                    if submission.is_prolonged()
                    else None
                )

                if expiration_day in [
                    submission.ends_at_max.date(),
                    prolongation_date,
                ]:
                    data = {
                        "subject": "{} ({})".format(
                            _("Votre autorisation arrive bientôt à échéance"),
                            submission.get_categories_names_list(),
                        ),
                        "users_to_notify": [submission.author.email],
                        "template": "submission_prolongation_reminder.txt",
                        "submission": submission,
                        "absolute_uri_func": Submission.get_absolute_url,
                        "forms_list": submission.get_forms_names_list(),
                    }
                    send_email_notification(data)

        logger.info("The submission expiration reminder Cronjob finished successfully")


class CleanupAnonymousRequests(CronJobBase):
    RUN_AT_TIMES = ["00:00"]
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = "submissions.anonymous_submission_cleanup"

    def do(self):
        try:
            # FIXME rename command (was `cleanup_anonymous_requests`)
            call_command("cleanup_anonymous_submissions")
        except CommandError:
            logger.error(
                "Error occured while trying to cleanup the anonymous submissions "
                "from the Cronjob."
            )
        else:
            logger.info(
                "The anonymous submissions cleanup Cronjob finished successfully"
            )


class SubmissionInquiryClosing(CronJobBase):
    RUN_AT_TIMES = ["15:00"]
    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = "submissions.submission_inquiry_closing"

    def do(self):
        inquiries_to_close = SubmissionInquiry.objects.filter(
            end_date=datetime.today().strftime("%Y-%m-%d")
        ).select_related("submission")

        for inquiry in inquiries_to_close:
            if not inquiry.submission.status == Submission.STATUS_INQUIRY_IN_PROGRESS:
                continue

            inquiry.submission.status = Submission.STATUS_PROCESSING
            inquiry.submission.save()

            data = {
                "subject": "{} ({})".format(
                    _("Fin de l'enquête publique"),
                    inquiry.submission.get_categories_names_list(),
                ),
                "users_to_notify": [
                    inquiry.submission.author.email,
                    inquiry.submitter.email,
                ],
                "submission": inquiry.submission,
                "absolute_uri_func": inquiry.submission.get_absolute_url,
                "template": "permit_request_inquiry_closing.txt",
                "objects_list": inquiry.submission.get_forms_names_list(),
            }
            send_email_notification(data)

        logger.info("The submission inquiry closing Cronjob finished")


class SubmissionInquiryOpening(CronJobBase):
    RUN_AT_TIMES = ["01:00"]
    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = "submissions.submission_inquiry_opening"

    def do(self):
        inquiries_to_open = SubmissionInquiry.objects.filter(
            start_date=datetime.today().strftime("%Y-%m-%d")
        ).select_related("submission")

        for inquiry in inquiries_to_open:
            if not inquiry.submission.status == Submission.STATUS_PROCESSING:
                continue

            inquiry.submission.status = Submission.STATUS_INQUIRY_IN_PROGRESS
            inquiry.submission.save()

        logger.info("The submission opening Cronjob finished")
