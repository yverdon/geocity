
from django.conf import settings
from django.db import models
from django.db.models.fields.files import FieldFile
from django.urls import reverse

from permits.fields import PrivateFileSystemStorage

class BackgroundFieldFile(FieldFile):
    @property
    def url(self):
        return reverse(
            "reports:background_download",
            kwargs={"path": self.name},
        )


class BackgroundFileField(models.FileField):
    """
    FileField storing information in a private media root.
    """

    attr_class = BackgroundFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs["storage"] = PrivateFileSystemStorage()
        super().__init__(verbose_name, name, **kwargs)