# Generated by Django 3.2.15 on 2022-11-21 14:41

from django.db import migrations


def reorder(apps, schema_editor):
    Form = apps.get_model("forms", "Form")
    for order, item in enumerate(Form.objects.all(), 1):
        item.order = order
        item.save(update_fields=["order"])


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0004_adapt_models_for_new_admin"),
    ]

    operations = [
        migrations.RunPython(reorder, reverse_code=migrations.RunPython.noop),
    ]
