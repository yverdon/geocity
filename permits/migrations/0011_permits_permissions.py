# Generated by Django 2.2.6 on 2020-05-07 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permits', '0010_permitrequestgeotime'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permitrequest',
            options={'permissions': [('amend_permit_request', 'Amender les demandes de permis'), ('validate_permit_request', 'Valider les demandes de permis')], 'verbose_name': 'demande de permis', 'verbose_name_plural': 'demandes de permis'},
        ),
        migrations.AlterField(
            model_name='permitrequest',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Brouillon'), (1, 'Envoyée, en attente de traitement'), (3, 'En traitement'), (2, 'Validée'), (4, 'Demande de compléments'), (5, 'En validation')], default=0, verbose_name='état'),
        ),
    ]
