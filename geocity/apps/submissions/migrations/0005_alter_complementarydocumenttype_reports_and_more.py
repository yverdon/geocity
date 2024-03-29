# Generated by Django 4.1 on 2022-11-22 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0015_alter_report_document_types_and_more"),
        ("submissions", "0004_new_admin_models_and_metadata"),
    ]

    operations = [
        migrations.AlterField(
            model_name="complementarydocumenttype",
            name="reports",
            field=models.ManyToManyField(
                blank=True, related_name="+", to="reports.report"
            ),
        ),
        migrations.AlterField(
            model_name="submission",
            name="contacts",
            field=models.ManyToManyField(
                related_name="+",
                through="submissions.SubmissionContact",
                to="submissions.contact",
            ),
        ),
    ]
