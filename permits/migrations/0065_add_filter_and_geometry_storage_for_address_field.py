# Generated by Django 3.2.13 on 2022-04-26 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('permits', '0064_add_field_can_always_update_in_WorksObjectType'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpermitrequestgeotime',
            name='worksobjectpropertyvalue',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='permits.worksobjectpropertyvalue', verbose_name="Champ de type adresse à l'origin de la géométrie"),
        ),
        migrations.AddField(
            model_name='permitrequestgeotime',
            name='worksobjectpropertyvalue',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='permits.worksobjectpropertyvalue', verbose_name="Champ de type adresse à l'origin de la géométrie"),
        ),
        migrations.AddField(
            model_name='worksobjectproperty',
            name='additional_searchtext_for_address_field',
            field=models.CharField(blank=True, help_text='Ex: "Yverdon-les-Bains" afin de limiter les recherches à Yverdon, <a href="https://api3.geo.admin.ch/services/sdiservices.html#search" target="_blank">Plus d\'informations</a>', max_length=255, verbose_name="Filtre additionnel pour la recherche d'adresse"),
        ),
        migrations.AddField(
            model_name='worksobjectproperty',
            name='store_geometry_for_address_field',
            field=models.BooleanField(default=False, verbose_name="Stocker la géométrie de l'adresse dans la table géométrique"),
        ),
    ]
