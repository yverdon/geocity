# Generated by Django 4.1.4 on 2022-12-12 16:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0016_change_admin_order"),
        ("forms", "0011_paymentsettings_integrator_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="historicalprice",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Tarif",
                "verbose_name_plural": "historical Tarifs",
            },
        ),
        migrations.AddField(
            model_name="paymentsettings",
            name="payment_confirmation_report",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="confirmation_payment_settings_objects",
                to="reports.report",
                verbose_name="Rapport pour la confirmation des paiements",
            ),
        ),
        migrations.AddField(
            model_name="paymentsettings",
            name="payment_refund_report",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="refund_payment_settings_objects",
                to="reports.report",
                verbose_name="Rapport pour le remboursement des paiements",
            ),
        ),
        migrations.AlterField(
            model_name="historicalprice",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
    ]
