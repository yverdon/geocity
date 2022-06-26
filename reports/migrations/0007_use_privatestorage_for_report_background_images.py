# Generated by Django 3.2.13 on 2022-06-26 08:33

import django.core.validators
from django.db import migrations

import permits.fields


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0006_auto_20220624_0236"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reportlayout",
            name="background",
            field=permits.fields.AdministrativeEntityFileField(
                blank=True,
                null=True,
                storage=permits.fields.PrivateFileSystemStorage(),
                upload_to="report_layout_backgrounds",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["png"]
                    )
                ],
                verbose_name='Image d\'arrière plan ("papier à en-tête")',
            ),
        ),
    ]
