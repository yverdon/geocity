# Generated by Django 3.2.13 on 2022-06-22 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("permits", "0076_remove_worksobjecttype_reports"),
        ("reports", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="report",
            name="type",
        ),
        migrations.RemoveField(
            model_name="report",
            name="work_object_types",
        ),
        migrations.AddField(
            model_name="report",
            name="document_types",
            field=models.ManyToManyField(
                blank=True,
                related_name="_reports_report_document_types_+",
                to="permits.ComplementaryDocumentType",
            ),
        ),
    ]