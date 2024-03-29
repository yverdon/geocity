# Generated by Django 4.2.1 on 2023-06-15 16:21
from django.db import migrations

from geocity.apps.api.services import convert_string_to_api_key


class Migration(migrations.Migration):
    def api_name_from_name(apps, schema_editor):

        Form = apps.get_model("forms", "Form")
        Field = apps.get_model("forms", "Field")

        for form in Form.objects.all():
            form.api_name = convert_string_to_api_key(form.name)
            form.save(update_fields=["api_name"])

        for field in Field.objects.all():
            field.api_name = convert_string_to_api_key(field.name)
            field.save(update_fields=["api_name"])

    def input_type_title_update(apps, schema_editor):
        Field = apps.get_model("forms", "Field")

        for field in Field.objects.all().filter(input_type="title"):
            field.input_type = "title_output"
            field.save(update_fields=["input_type"])

    dependencies = [
        (
            "forms",
            "0021_field_api_name_form_api_name",
        ),
    ]

    operations = [
        migrations.RunPython(api_name_from_name),
        migrations.RunPython(input_type_title_update),
    ]
