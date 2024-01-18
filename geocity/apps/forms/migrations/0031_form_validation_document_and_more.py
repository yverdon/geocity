# Generated by Django 4.2.9 on 2024-01-18 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0030_form_default_validation_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="form",
            name="validation_document",
            field=models.BooleanField(
                default=True, verbose_name="Document de validation"
            ),
        ),
        migrations.AddField(
            model_name="form",
            name="validation_document_required_for",
            field=models.IntegerField(
                choices=[(1, "Approbation"), (2, "Refus"), (3, "Approbation et refus")],
                default=1,
                verbose_name="Document de validation obligatoire pour",
            ),
        ),
    ]
