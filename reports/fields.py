import datetime
import posixpath

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.fields.files import FieldFile
from django.urls import reverse


class PrivateFileSystemStorage(FileSystemStorage):
    """
    Storage for files that MUST NOT get directly exposed by the web server.
    """

    def __init__(self):
        super().__init__(location=settings.PRIVATE_MEDIA_ROOT, base_url=None)


class ReportLayoutFieldFile(FieldFile):
    @property
    def url(self):
        return reverse(
            "reporst:report_layout_file_download",
            kwargs={"path": self.name},
        )


class ReportLayoutFileField(models.FileField):
    """
    FileField storing information in a private media root.
    """

    attr_class = ReportLayoutFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs["storage"] = PrivateFileSystemStorage()
        super().__init__(verbose_name, name, **kwargs)