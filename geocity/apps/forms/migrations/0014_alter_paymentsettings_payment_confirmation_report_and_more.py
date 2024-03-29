# Generated by Django 4.1.4 on 2022-12-19 16:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0018_alter_sectionparagraph_content_and_more"),
        ("forms", "0013_alter_formprice_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentsettings",
            name="payment_confirmation_report",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="confirmation_payment_settings_objects",
                to="reports.report",
                verbose_name="Rapport pour la confirmation des paiements",
            ),
        ),
        migrations.AlterField(
            model_name="paymentsettings",
            name="payment_refund_report",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="refund_payment_settings_objects",
                to="reports.report",
                verbose_name="Rapport pour le remboursement des paiements",
            ),
        ),
    ]
