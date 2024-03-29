# Generated by Django 4.1 on 2022-12-04 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0007_alter_formprice_options_formprice_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentsettings",
            name="api_key",
            field=models.CharField(default=1, max_length=255, verbose_name="API key"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="paymentsettings",
            name="payment_processor",
            field=models.CharField(
                choices=[("PostFinance", "PostFinance Checkout")],
                default="PostFinance",
                max_length=255,
                verbose_name="Processeur de paiement",
            ),
        ),
        migrations.AddField(
            model_name="paymentsettings",
            name="space_id",
            field=models.CharField(default=1, max_length=255, verbose_name="Space ID"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="paymentsettings",
            name="user_id",
            field=models.CharField(default=1, max_length=255, verbose_name="User ID"),
            preserve_default=False,
        ),
    ]
