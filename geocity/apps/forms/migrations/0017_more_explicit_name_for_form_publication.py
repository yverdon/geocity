# Generated by Django 4.1.4 on 2023-01-20 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0016_alter_historicalprice_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="form",
            name="is_public",
            field=models.BooleanField(
                default=False,
                verbose_name="Formulaire public",
            ),
        ),
    ]