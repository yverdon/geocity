from permits import models
from django.core import management
from django.core.management.base import BaseCommand


def update_default_print_config():

    for wot in models.WorksObjectType.objects.all():
        wot.qgisproject_set.update(
            qgis_project_file="report_template.qgs",
            qgis_print_template_name="print_template",
            description="Impression standard",
        )
        wot.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Updating default print configuration for work object types")
        update_default_print_config()
