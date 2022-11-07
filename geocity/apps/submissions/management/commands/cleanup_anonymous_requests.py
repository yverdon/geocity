import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext

from geocity.apps.submissions.models import Submission


class Command(BaseCommand):
    help = gettext(
        "Delete any anonymous submissions and associated temporary users that are not "
        "validated and older than %s hours."
        % settings.PENDING_ANONYMOUS_REQUEST_MAX_AGE
    )

    def handle(self, *args, **options):
        self.stdout.write(
            "Deleting old pending anonymous submissions and temporary users..."
        )

        permit_requests_to_delete = Submission.objects.select_related("author").filter(
            created_at__lt=timezone.now()
            - datetime.timedelta(hours=settings.PENDING_ANONYMOUS_REQUEST_MAX_AGE),
            author__username__startswith=settings.TEMPORARY_USER_PREFIX,
        )
        authors_to_delete = set(
            permit_requests_to_delete.values_list("author_id", flat=True)
        )

        with transaction.atomic():
            permit_requests_to_delete.delete()
            get_user_model().objects.filter(id__in=authors_to_delete).delete()

        self.stdout.write("Cleanup successful.")
