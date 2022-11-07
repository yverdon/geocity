# This could fail if the code has diverged from old migrations because we cannot use
# historical models. Since this data migration is not critical, we swallow exceptions,
# to avoid breaking migrations down the line.
from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from django.db import transaction
from django.utils.translation import gettext

from geocity.apps.reports.signals import create_default_report_for_integrator


class Command(BaseCommand):

    help = gettext("Create default print template for integrators.")

    def handle(self, *args, **options):
        self.stdout.write("Creating default print template for integrator ...")

        with transaction.atomic():
            for integrator in Group.objects.all():
                create_default_report_for_integrator(Group, integrator, True)
