from django.contrib.auth.models import Group
from django.core.management import BaseCommand, CommandError
from django.utils.translation import gettext

from geocity.apps.accounts.users import get_integrator_permissions


class Command(BaseCommand):

    help = gettext(
        "Update the permissions for Groups that have is_integrator_admin = True set in the admin."
    )

    def handle(self, *args, **options):
        self.stdout.write("Adding new permissions ...")

        try:
            integrator_groups = Group.objects.filter(
                permit_department__is_integrator_admin=True
            )

            for integrator_group in integrator_groups:
                integrator_group.permissions.set(get_integrator_permissions())

            self.stdout.write("Update of integrator permissions successful.")
        except CommandError:
            self.stdout.write("ERROR: Error while updating integrator permissions!")
