# Generated by Django 3.1.4 on 2021-01-28 09:58

from django.db import migrations, models


def reorder(apps, schema_editor):
    WorksObjectProperty = apps.get_model("permits", "worksobjectproperty")
    for index, item in enumerate(WorksObjectProperty.objects.order_by("order", "name")):
        item.order = index
        item.save()


class Migration(migrations.Migration):
    dependencies = [
        ("permits", "0015_works_object_properties_order"),
    ]

    operations = [
        migrations.RunPython(reorder),
    ]
