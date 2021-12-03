from permits import models
from django.core import management
from django.core.management.base import BaseCommand


def add_default_print_config():

    for wot in models.WorksObjectType.objects.all():
        wot.qgisproject_set.create(
            qgis_project_file="report_template.qgs",
            qgis_print_template_name="print_template",
            description="Impression standard",
        )
        wot.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(
            "Adding default print configuration for work object types that have none"
        )
        add_default_print_config()
