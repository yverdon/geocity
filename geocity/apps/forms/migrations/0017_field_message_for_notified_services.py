# Generated by Django 4.1.4 on 2023-02-02 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0016_alter_historicalprice_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="field",
            name="message_for_notified_services",
            field=models.CharField(
                blank=True,
                max_length=255,
                verbose_name="Message transmis aux services notifiés",
            ),
        ),
    ]