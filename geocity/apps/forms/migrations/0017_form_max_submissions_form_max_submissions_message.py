# Generated by Django 4.1.4 on 2023-01-25 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0016_alter_historicalprice_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="form",
            name="max_submissions",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Nombre maximum de demandes"
            ),
        ),
        migrations.AddField(
            model_name="form",
            name="max_submissions_message",
            field=models.CharField(
                blank=True,
                default="Ce formulaire est désactivé car le nombre maximal de soumissions a été atteint.",
                max_length=300,
                null=True,
                verbose_name="Message lorsque le nombre maximal est atteint",
            ),
        ),
    ]