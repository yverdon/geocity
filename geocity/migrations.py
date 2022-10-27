import functools
import operator

from django.contrib.auth.management import create_permissions
from django.contrib.contenttypes.management import create_contenttypes
from django.db import migrations


def copy_tags(apps, from_obj, to_obj):
    TaggedItem = apps.get_model("taggit", "TaggedItem")
    ContentType = apps.get_model("contenttypes", "ContentType")

    content_type = ContentType.objects.get(
        app_label=to_obj._meta.app_label,
        model=to_obj._meta.model_name,
    )

    for tagged_item in TaggedItem.objects.filter(
        content_type__app_label=from_obj._meta.app_label,
        content_type__model=from_obj._meta.model_name,
        object_id=from_obj.id,
    ):
        TaggedItem.objects.create(
            content_type=content_type, object_id=to_obj.id, tag_id=tagged_item.tag_id
        )


def sync_sequence(table_name, field="id"):
    return migrations.RunSQL(
        f"""
        SELECT SETVAL(
            PG_GET_SERIAL_SEQUENCE('{table_name}', '{field}'),
            COALESCE(MAX("{field}"), 1)
        ) FROM {table_name}"""
    )


def migrate_contenttypes(apps, schema_editor):
    """
    The content types from the `forms` app are not available in this migration if it’s
    run during the same run as the initial migration (content types are created at the
    post-migration step).

    Since we need content types (to copy the tags), we need to make sure they exist
    here.
    """
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_contenttypes(app_config, apps=apps, verbosity=0)
        app_config.models_module = None


def migrate_permissions(apps, schema_editor):
    """
    The new permissions are not available a migration run during the same run as the
    initial migration (permissions are created at the post-migration step).

    Since we need permissions (to reattribute them), we need to make sure they exist
    here.
    """
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None


def model_fields_in_common(*models):
    """
    Return the intersection of the names of the fields of the given models.

    Example:

    >>> class ModelA(models.Model):
    ...     first_name = ...
    ...     last_name = ...
    >>> class ModelB(models.Model):
    ...     first_name = ...
    ...     address = ...
    >>> model_fields_in_common(ModelA, ModelB)
    {'first_name'}
    """
    fields = (
        set(field.get_attname() for field in model._meta.fields) for model in models
    )
    return functools.reduce(operator.and_, fields)


def fields_values(fields_names, model_instance):
    return {
        field_name: getattr(model_instance, field_name) for field_name in fields_names
    }


def common_fields_values(model1, model2_instance):
    return fields_values(
        model_fields_in_common(model1, model2_instance), model2_instance
    )


def copy_model(old_model, new_model):
    new_objs = [
        new_model(**common_fields_values(new_model, old_obj))
        for old_obj in old_model.objects.all()
    ]

    new_model.objects.bulk_create(new_objs)


def bulk_create(generator):
    objects = list(generator)

    if len(objects) == 0:
        return

    type(objects[0]).objects.bulk_create(objects)
