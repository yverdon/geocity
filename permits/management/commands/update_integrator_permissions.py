from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand, CommandError
from django.utils.translation import gettext

from permits import admin


class Command(BaseCommand):

    help = gettext(
        "Update the permissions for Groups that have is_integrator_admin = True set in the admin."
        "This command is usefule when new models are added to INTEGRATOR_PERMITS_MODELS_PERMISSIONS in admin.py"
    )

    def handle(self, *args, **options):
        self.stdout.write("Adding new permissions ...")

        try:
            integrator_groups = Group.objects.filter(
                permitdepartment__is_integrator_admin=True
            )

            permits_permissions = Permission.objects.filter(
                content_type__app_label="permits",
                content_type__model__in=admin.INTEGRATOR_PERMITS_MODELS_PERMISSIONS,
            )

            other_permissions = Permission.objects.filter(
                codename__in=admin.OTHER_PERMISSIONS_CODENAMES
            )

            for integrator_group in integrator_groups:

                # set the required permissions for the integrator group
                integrator_group.permissions.set(
                    permits_permissions.union(other_permissions)
                )
            self.stdout.write("Update of intergrator permissions sucessful.")
        except CommandError:
            self.stdout.write("ERROR: Error while updating intergrator permissions!")
