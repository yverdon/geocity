# Generated by Django 4.1 on 2022-12-10 12:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("forms", "0010_alter_form_requires_online_payment_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentsettings",
            name="integrator",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="auth.group",
                verbose_name="Groupe des administrateurs",
            ),
        ),
        migrations.AlterField(
            model_name="form",
            name="requires_online_payment",
            field=models.BooleanField(
                default=False,
                help_text="Requiert la présence de <strong>paramètres de paiement</strong>, d'au moins un <strong>tarif</strong>, et de <strong>ne pas être soumis à des frais</strong>.",
                verbose_name="Soumis au paiement en ligne",
            ),
        ),
    ]
