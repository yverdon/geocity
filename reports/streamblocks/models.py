from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField

from permits.fields import AdministrativeEntityFileField


class PrintBlockRichText(models.Model):
    content = RichTextField(
        # TODO: reverse_lazy and parametrize URL instead of hardcode
        # TODO WIP: use rich text editor
        help_text=_(
            'You can access the contents of the data returned by the API with placeholders like `{{data.properties.geotime_aggregated.start_date}}`. Have a look at <a href="http://localhost:9095/wfs3/collections/permits/items/1">the API</a> to see available data.'
        )
    )


class PrintBlockCustom(models.Model):
    content = models.TextField(
        # TODO: reverse_lazy and parametrize URL instead of hardcode
        help_text=_(
            'You can access the contents of the data returned by the API with placeholders like `{{data.properties.geotime_aggregated.start_date}}`. Have a look at <a href="http://localhost:9095/wfs3/collections/permits/items/1">the API</a> to see available data.'
        )
    )


class PrintBlockMap(models.Model):
    qgis_project_file = AdministrativeEntityFileField(
        _("Projet QGIS '*.qgs'"),
        validators=[FileExtensionValidator(allowed_extensions=["qgs"])],
        upload_to="qgis_templates",
    )
    qgis_print_template_name = models.CharField(
        _("Nom du template d'impression QGIS"), max_length=150,
    )


class PrintBlockContacts(models.Model):
    content = models.TextField()


class PrintBlockValidation(models.Model):
    content = models.TextField()


class PrintBlockRawData(models.Model):
    class Meta:
        abstract = True


class PrintBlockPageBreak(models.Model):
    class Meta:
        abstract = True


# Register blocks for StreamField as list of models
STREAMBLOCKS_MODELS = [
    PrintBlockRichText,
    PrintBlockMap,
    PrintBlockContacts,
    PrintBlockValidation,
    PrintBlockRawData,
    PrintBlockPageBreak,
    PrintBlockCustom,
]
