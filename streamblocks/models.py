from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

class PrintBlockParagraph(models.Model):
    title = models.CharField(max_length=1000)
    content = models.TextField(
        # TODO: reverse_lazy and parametrize URL instead of hardcode
        help_text=_(
        "You can access the contents of the data returned by the API with placeholders like `{{data.properties.geotime_aggregated.start_date}}`. Have a look at <a href=\"http://localhost:9095/wfs3/collections/permits/items/1\">the API</a> to see available data."
        )
    )

class PrintBlockMap(models.Model):
    url = models.CharField(max_length=1000)

class PrintBlockContacts(models.Model):
    content = models.TextField()

class PrintBlockValidation(models.Model):
    content = models.TextField()

# Register blocks for StreamField as list of models
STREAMBLOCKS_MODELS = [
    PrintBlockParagraph,
    PrintBlockMap,
    PrintBlockContacts,
    PrintBlockValidation,
]
