# Generated by Django 3.1.4 on 2021-01-27 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("permits", "0012_permit_actor_mandatory"),
    ]

    operations = [
        migrations.AlterField(
            model_name="worksobjectproperty",
            name="input_type",
            field=models.CharField(
                choices=[
                    ("text", "Texte"),
                    ("checkbox", "Case à cocher"),
                    ("number", "Nombre"),
                    ("file", "Fichier"),
                    ("address", "Adresse"),
                    ("date", "Date"),
                ],
                max_length=30,
                verbose_name="type de caractéristique",
            ),
        ),
    ]
