# Generated by Django 4.1 on 2022-12-14 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("submissions", "0007_remove_geom_layer"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalsubmission",
            name="intersected_geometries",
        ),
        migrations.RemoveField(
            model_name="submission",
            name="intersected_geometries",
        ),
    ]