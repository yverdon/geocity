from django.contrib.sites.models import Site
from django.core.management import BaseCommand, CommandError
from django.utils.translation import gettext


class Command(BaseCommand):

    help = gettext(
        "Create a site whose name corresponds to the django container 'web'."
    )

    def handle(self, *args, **options):
        self.stdout.write("Creating 'web' site ...")

        try:
            Site.objects.update_or_create(domain="web", name="web (internal calls)")
            self.stdout.write("Creation of default 'web' site successful.")
        except CommandError:
            self.stdout.write(
                "ERROR: Error while creating 'web' site, print will not work !"
            )
