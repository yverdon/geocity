from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand, CommandError
from django.db import IntegrityError, transaction
from django.utils.translation import gettext

from geocity.apps.permits.models import PermitAdministrativeEntity, PermitAuthor


def _create_anonymous_user_for_entity(entity):
    try:
        entity.anonymous_user
    except ObjectDoesNotExist:
        username = "%s%s" % (settings.ANONYMOUS_USER_PREFIX, entity.pk)
        first_name = "Anonymous user"
        last_name = entity.name

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_active=False,
        )
        user.save()

        PermitAuthor(
            administrative_entity=entity,
            user_id=user.id,
            zipcode=settings.ANONYMOUS_USER_ZIPCODE,
        ).save()


class Command(BaseCommand):
    help = gettext("Create anonymous users in PermitAdministrativeEntity")

    def add_arguments(self, parser):
        parser.add_argument(
            "entity_ids",
            nargs="*",
            type=int,
            help=gettext(
                "A list of ids, of administrative entity in which to create "
                "related anonymous users. If no id is provided, an anonymous user "
                "is created in each administrative entities. In any case, anonymous "
                "user will be created in an entity only if it doesn't exist yet."
            ),
        )

    def handle(self, *args, **options):
        self.stdout.write(
            "Create an anonymous user for each PermitAdministrativeEntity..."
        )

        if options["entity_ids"]:
            entities = PermitAdministrativeEntity.objects.filter(
                pk__in=options["entity_ids"]
            )
        else:
            entities = PermitAdministrativeEntity.objects.all()

        with transaction.atomic():
            try:
                for entity in entities:
                    _create_anonymous_user_for_entity(entity)
            except IntegrityError:
                raise CommandError

        self.stdout.write("Anonymous users successfully created.")
