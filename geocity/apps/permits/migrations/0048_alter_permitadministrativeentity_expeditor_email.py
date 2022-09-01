# Generated by Django 3.2.7 on 2021-10-21 14:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("permits", "0047_alter_worksobjecttype_start_delay"),
    ]

    operations = [
        migrations.AlterField(
            model_name="permitadministrativeentity",
            name="expeditor_email",
            field=models.CharField(
                blank=True,
                max_length=255,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Le format de l'adresse email n'est pas valable.",
                        regex="^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$",
                    )
                ],
                verbose_name="Adresse email de l'expéditeur des notifications",
            ),
        ),
    ]