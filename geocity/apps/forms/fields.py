from django.db import models
from django.db.models.fields.files import FieldFile
from django.urls import reverse

from geocity.fields import PrivateFileSystemStorage


class AdministrativeEntityFieldFile(FieldFile):
    @property
    def url(self):
        return reverse(
            "permits:administrative_entity_file_download",
            kwargs={"path": self.name},
        )


class AdministrativeEntityFileField(models.FileField):
    """
    FileField storing information in a private media root.
    """

    attr_class = AdministrativeEntityFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs["storage"] = PrivateFileSystemStorage()
        super().__init__(verbose_name, name, **kwargs)


class FormFieldFile(FieldFile):
    @property
    def url(self):
        return reverse(
            "permits:works_object_property_file_download",
            kwargs={"path": self.name},
        )


class FormFileField(models.FileField):
    """
    FileField storing information in a private media root.
    """

    attr_class = FormFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs["storage"] = PrivateFileSystemStorage()
        super().__init__(verbose_name, name, **kwargs)
