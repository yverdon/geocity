from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand, CommandError
from django.utils.translation import gettext

from geocity.apps.accounts import permissions_groups


class Command(BaseCommand):

    help = gettext(
        "Update the permissions for Groups that have is_integrator_admin = True set in the admin."
        "This command is useful when new models are added to INTEGRATOR_REQUIRED_MODELS_PERMISSIONS in permits/admin.py"
        "or to INTEGRATOR_REPORTS_MODELS_PERMISSIONS in reports/admin.py"
    )

    def handle(self, *args, **options):
        self.stdout.write("Adding new permissions ...")

        try:
            integrator_groups = Group.objects.filter(
                permitdepartment__is_integrator_admin=True
            )

            permits_permissions = Permission.objects.filter(
                content_type__app_label="permits",
                content_type__model__in=permissions_groups.INTEGRATOR_REQUIRED_MODELS_PERMISSIONS,
            )

            report_permissions = Permission.objects.filter(
                content_type__app_label="reports",
                content_type__model__in=permissions_groups.INTEGRATOR_REPORTS_MODELS_PERMISSIONS,
            )

            other_permissions = Permission.objects.filter(
                codename__in=permissions_groups.OTHER_PERMISSIONS_CODENAMES
            )

            for integrator_group in integrator_groups:
                # set the required permissions for the integrator group
                integrator_group.permissions.set(
                    permits_permissions.union(other_permissions).union(
                        report_permissions
                    )
                )
            self.stdout.write("Update of integrator permissions sucessful.")
        except CommandError:
            self.stdout.write("ERROR: Error while updating integrator permissions!")
