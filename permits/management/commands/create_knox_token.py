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

        if options["user_id"]:
            user = User.objects.get(id=options["user_id"][0])
        else:
            raise CommandError

        with transaction.atomic():
            try:
                authtoken, token = AuthToken.objects.create(user, expiry=None)
            except IntegrityError:
                raise CommandError

        self.stdout.write("Knox token successfully created.")
        return token
