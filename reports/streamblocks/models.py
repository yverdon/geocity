from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField

from permits.fields import AdministrativeEntityFileField


class PrintBlockRichText(models.Model):
    content = RichTextField(
        # TODO: reverse_lazy and parametrize URL instead of hardcode
        # TODO WIP: use rich text editor
        help_text=(
            _(
                "Il est possible d'accéder aux données de l'API avec la syntaxe suivante: `{{data.properties.geotime_aggregated.start_date}}`. Consultez les résults de <a href=\"http://localhost:9095/wfs3/collections/permits/items/1\">l'API</a> pour voir les données disponibles."
            )
            + "\n"
            + _(
                "ATTENTION: l'accès à ce type de bloc doit être réservé aux utilisateurs approuvés puisque l'implémentation actuelle n'est pas sécurisée."
            )
        )
    )


class PrintBlockCustom(models.Model):
    content = models.TextField(
        # TODO: reverse_lazy and parametrize URL instead of hardcode
        help_text=(
            _(
                "Il est possible d'accéder aux données de l'API avec la syntaxe suivante: `{{data.properties.geotime_aggregated.start_date}}`. Consultez les résults de <a href=\"http://localhost:9095/wfs3/collections/permits/items/1\">l'API</a> pour voir les données disponibles."
            )
            + "\n"
            + _(
                "ATTENTION: l'accès à ce type de bloc doit être réservé aux utilisateurs approuvés puisque l'implémentation actuelle n'est pas sécurisée."
            )
        )
    )


class PrintBlockMap(models.Model):
    qgis_project_file = AdministrativeEntityFileField(
        _("Projet QGIS '*.qgs'"),
        validators=[FileExtensionValidator(allowed_extensions=["qgs"])],
        upload_to="qgis_templates",
    )
    qgis_print_template_name = models.CharField(
        _("Nom du template d'impression QGIS"),
        max_length=150,
        help_text=_(
            "ATTENTION: l'accès à ce type de bloc doit être réservé aux utilisateurs approuvés puisque l'implémentation actuelle n'est pas sécurisée."
        ),
    )


class PrintBlockContacts(models.Model):
    content = models.TextField(_("Liste des contacts"))


class PrintBlockValidation(models.Model):
    content = models.TextField()


class PrintBlockRecipient(models.Model):
    class Meta:
        abstract = True


class PrintBlockRawData(models.Model):
    class Meta:
        abstract = True


class PrintBlockPageBreak(models.Model):
    class Meta:
        abstract = True


class PrintBlockAuthors(models.Model):
    content = models.TextField


class PrintBlockDetails(models.Model):
    content = models.TextField


class PrintBlockPlanning(models.Model):
    content = models.TextField


# class PrintBlockFiles(models.Model):
#     content = models.TextField


class PrintBlockHorizontalRule(models.Model):
    class Meta:
        abstract = True


# Register blocks for StreamField as list of models
STREAMBLOCKS_MODELS = [
    PrintBlockRichText,
    PrintBlockMap,
    PrintBlockContacts,
    PrintBlockValidation,
    PrintBlockRecipient,
    PrintBlockRawData,
    PrintBlockPageBreak,
    PrintBlockCustom,
    PrintBlockAuthors,
    PrintBlockDetails,
    PrintBlockPlanning,
    # PrintBlockFiles,
    PrintBlockHorizontalRule,
]
