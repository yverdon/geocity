import datetime
import os
import posixpath

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.fields.files import FieldFile
from django.template.defaultfilters import slugify
from django.urls import reverse

from geocity.fields import PrivateFileSystemStorage


class SubmissionFieldFile(FieldFile):
    @property
    def url(self):
        return reverse(
            "submissions:submission_file_download",
            kwargs={"path": self.name},
        )


class SubmissionFileField(models.FileField):
    """
    FileField storing information in a private media root.
    """

    attr_class = SubmissionFieldFile

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


class ArchiveFileSystemStorage(FileSystemStorage):
    """
    Storage for files that MUST NOT get directly exposed by the web server.
    """

    def __init__(self):
        super().__init__(location=settings.ARCHIVE_ROOT, base_url=None)


class ArchiveDocumentFieldFile(FieldFile):
    @property
    def url(self):
        return reverse(
            "submissions:complementary_documents_download",
            kwargs={"path": self.name},
        )


def archive_upload_to(instance, filename):
    _, ext = os.path.splitext(filename)
    t = instance.archived_date or datetime.datetime.now()
    archived_date = t.strftime("%d.%m.%Y.%H.%M.%S")
    return f"{instance.submission.id:02d}_{archived_date}_{slugify(instance.submission.get_categories_names_list())}{ext}"


class ArchiveDocumentFileField(models.FileField):
    """
    FileField storing information in a private media root.
    """

    attr_class = ArchiveDocumentFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs["storage"] = ArchiveFileSystemStorage()
        kwargs["upload_to"] = archive_upload_to
        super().__init__(verbose_name, name, **kwargs)


class ComplementaryDocumentFieldFile(FieldFile):
    @property
    def url(self):
        return reverse(
            "submissions:complementary_documents_download",
            kwargs={"path": self.name},
        )


class ComplementaryDocumentFileField(models.FileField):
    """
    FileField storing information in a private media root.
    """

    attr_class = ComplementaryDocumentFieldFile

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs["storage"] = PrivateFileSystemStorage()
        super().__init__(verbose_name, name, **kwargs)
