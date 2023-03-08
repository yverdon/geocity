from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations


def forwards_func(apps, schema_editor):
    FieldModel = apps.get_model("forms", "Field")
    FieldModelTranslation = apps.get_model("forms", "FieldTranslation")

    for obj in FieldModel.objects.all():
        FieldModelTranslation.objects.create(
            master_id=obj.pk,
            language_code=settings.PARLER_DEFAULT_LANGUAGE_CODE,
            name=obj._name,
            placeholder=obj._placeholder,
            help_text=obj._help_text,
            choices=obj._choices,
        )


def backwards_func(apps, schema_editor):
    FieldModel = apps.get_model("forms", "Field")
    FieldModelTranslation = apps.get_model("forms", "FieldTranslation")

    for obj in FieldModel.objects.all():
        translation = _get_translation(obj, FieldModelTranslation)
        obj._name = translation.name
        obj.save()


def _get_translation(obj, FieldModelTranslation):
    translations = FieldModelTranslation.objects.filter(master_id=obj.pk)
    try:
        # Try default translation
        return translations.get(language_code=settings.LANGUAGE_CODE)
    except ObjectDoesNotExist:
        try:
            # Try default language
            return translations.get(language_code=settings.PARLER_DEFAULT_LANGUAGE_CODE)
        except ObjectDoesNotExist:
            # Maybe the object was translated only in a specific language?
            # Hope there is a single translation
            return translations.get()


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0019_add_translated_fields_to_form"),
    ]

    operations = [
        migrations.RunPython(forwards_func, backwards_func),
    ]
