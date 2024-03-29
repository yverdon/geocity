# Generated by Django 4.2.1 on 2023-06-13 11:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("submissions", "0017_alter_submission_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalsubmission",
            name="sent_date",
            field=models.DateTimeField(null=True, verbose_name="date du dernier envoi"),
        ),
        migrations.AddField(
            model_name="submission",
            name="sent_date",
            field=models.DateTimeField(null=True, verbose_name="date du dernier envoi"),
        ),
        migrations.AlterField(
            model_name="submissioninquiry",
            name="submission",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="inquiries",
                to="submissions.submission",
                verbose_name="Demande",
            ),
        ),
    ]
