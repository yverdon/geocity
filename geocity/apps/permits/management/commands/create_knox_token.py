from django.contrib.auth.models import User
from django.core.management import BaseCommand, CommandError
from django.db import IntegrityError, transaction
from django.utils.translation import gettext
from knox.models import AuthToken


class Command(BaseCommand):
    help = gettext("Create knox token")

    def add_arguments(self, parser):
        parser.add_argument(
            "user_id",
            nargs="*",
            type=int,
            help=gettext("User to create the knox token"),
        )

    def handle(self, *args, **options):
        self.stdout.write("Create a knox token for the current User...")

        user_id = options["user_id"][0]
        request_user_id = options["user_id"][1]

        # TODO: Add permissions (on model) to create token of another user, if needed
        # Prevent the creation of the knox token on another user than himself
        if user_id and user_id == request_user_id:
            user = User.objects.get(id=user_id)
        else:
            raise CommandError
        # TODO: Define when a token needs to be deleted
        with transaction.atomic():
            try:
                authtoken, token = AuthToken.objects.create(user, expiry=None)
            except IntegrityError:
                raise CommandError

        self.stdout.write("Knox token successfully created.")
        return token
