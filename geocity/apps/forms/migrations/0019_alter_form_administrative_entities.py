# Generated by Django 4.1.7 on 2023-05-16 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0013_permitdepartment_generic_email_and_more"),
        ("forms", "0018_alter_historicalprice_amount_alter_price_amount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="form",
            name="administrative_entities",
            field=models.ManyToManyField(
                related_name="forms",
                to="accounts.administrativeentity",
                verbose_name="entité administrative",
            ),
        ),
    ]