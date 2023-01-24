# Generated by Django 4.1.4 on 2023-01-18 10:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_alter_administrativeentity_integrator_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="siteprofile",
            options={
                "verbose_name": "Paramètres complémentaires (à définir après avoir créé le site)",
                "verbose_name_plural": "Paramètres complémentaires (à définir après avoir créé le site)",
            },
        ),
        migrations.AddField(
            model_name="siteprofile",
            name="custom_template",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="accounts.templatecustomization",
                verbose_name="Page de login",
            ),
        ),
    ]
