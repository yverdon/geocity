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


class PermitRequestFieldFile(FieldFile):
    @property
    def url(self):
        return reverse(
            "permits:permit_request_file_download", kwargs={"path": self.name},
        )


class PermitRequestFileField(models.FileField):
    """
    FileField storing information in a private media root.
    """

    attr_class = PermitRequestFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs["storage"] = PrivateFileSystemStorage()
        super().__init__(verbose_name, name, **kwargs)

    def generate_filename(self, instance, filename):
        """
        Override `FileField.generate_filename` to prefix the filename with the id of the permit request. This means such
        file fields *cannot* be used until the permit request instance has an id (ie. is persisted in the database).
        """
        if not instance.pk:
            raise ValueError(
                "Permit request must be saved before this file field can be used"
            )

        if callable(self.upload_to):
            filename = self.upload_to(instance, filename)
        else:
            dirname = datetime.datetime.now().strftime(str(self.upload_to))
            filename = posixpath.join(dirname, filename)

        # Prefix the generated filename with the id of the permit request
        filename = posixpath.join(str(instance.pk), filename)

        return self.storage.generate_filename(filename)


class AdministrativeEntityFieldFile(FieldFile):
    @property
    def url(self):
        return reverse(
            "permits:administrative_entity_file_download", kwargs={"path": self.name},
        )


class AdministrativeEntityFileField(models.FileField):
    """
    FileField storing information in a private media root.
    """

    attr_class = AdministrativeEntityFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs["storage"] = PrivateFileSystemStorage()
        super().__init__(verbose_name, name, **kwargs)
