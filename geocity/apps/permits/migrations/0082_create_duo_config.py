# Generated by Django 3.2.15 on 2022-09-26 08:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("permits", "0082_add_visible_by_validators_for_amend_property"),
    ]

    operations = [
        migrations.CreateModel(
            name="DuoConfig",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=128, blank=True, verbose_name="name"),
                ),
                (
                    "description",
                    models.CharField(max_length=128, verbose_name="description"),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Décocher afin de désactiver cette configuration. Les groupes ayant cette configuration, ne seront plus redirigés vers duo",
                        verbose_name="Actif",
                    ),
                ),
                (
                    "client_id",
                    models.CharField(max_length=254, verbose_name="Client id pour duo"),
                ),
                (
                    "client_secret",
                    models.CharField(
                        max_length=254, verbose_name="Client secret pour duo"
                    ),
                ),
                (
                    "host",
                    models.CharField(max_length=254, verbose_name="Host pour duo"),
                ),
                (
                    "integrator",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="auth.group",
                        verbose_name="Groupe des administrateurs",
                    ),
                ),
            ],
            options={
                "verbose_name": "4.2 Configuration du client duo",
                "verbose_name_plural": "4.2 Configuration des clients duo",
            },
        ),
        migrations.AddField(
            model_name="permitdepartment",
            name="duo_config",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="duo",
                to="permits.duoconfig",
                verbose_name="Configuration duo. Devient obligatoire si assigné avec un 2fa obligatoire",
            ),
        ),
    ]
