# Generated by Django 3.2.13 on 2022-05-04 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permits', '0067_fix_verbose_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='permitadministrativeentity',
            name='additional_searchtext_for_address_field',
            field=models.CharField(blank=True, help_text='Ex: "Yverdon-les-Bains" afin de limiter les recherches à Yverdon, <a href="https://api3.geo.admin.ch/services/sdiservices.html#search" target="_blank">Plus d\'informations</a>', max_length=255, verbose_name="Filtre additionnel pour la recherche d'adresse"),
        ),
    ]
