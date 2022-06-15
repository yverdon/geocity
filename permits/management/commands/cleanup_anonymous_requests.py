import datetime

from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.utils.translation import gettext

from permits.models import PermitRequest


class Command(BaseCommand):
    help = gettext(
        "Delete any anonymous requests and associated temporary users that are not "
        "validated and older than %s hours."
        % settings.PENDING_ANONYMOUS_REQUEST_MAX_AGE
    )

    def handle(self, *args, **options):
        self.stdout.write(
            "Deleting old pending an anonymous requests and temporary users..."
        )

        permit_requests = list(
            PermitRequest.objects.prefetch_related("author").filter(
                created_at__lt=timezone.now()
                - datetime.timedelta(hours=settings.PENDING_ANONYMOUS_REQUEST_MAX_AGE),
                author__user__username__startswith=settings.TEMPORARY_USER_PREFIX,
            )
        )

        with transaction.atomic():
            try:
                while len(permit_requests) > 0:
                    permit_request = permit_requests.pop()
                    author = permit_request.author
                    permit_request.delete()
                    author.user.delete()
            except IntegrityError:
                raise CommandError

        self.stdout.write("Cleanup successful.")
