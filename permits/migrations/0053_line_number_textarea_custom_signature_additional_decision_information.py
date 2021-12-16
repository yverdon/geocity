# Generated by Django 3.2.7 on 2021-12-16 11:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permits', '0052_add_email_domains_list_for_admin_filtering'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permitadministrativeentity',
            name='logo_main',
        ),
        migrations.RemoveField(
            model_name='permitadministrativeentity',
            name='logo_secondary',
        ),
        migrations.RemoveField(
            model_name='permitadministrativeentity',
            name='title_signature_1',
        ),
        migrations.RemoveField(
            model_name='permitadministrativeentity',
            name='title_signature_2',
        ),
        migrations.AddField(
            model_name='historicalpermitrequest',
            name='additional_decision_information',
            field=models.TextField(blank=True, help_text='Facultative, sera transmise au requérant', max_length=2048, verbose_name='Information complémentaire'),
        ),
        migrations.AddField(
            model_name='permitadministrativeentity',
            name='custom_signature',
            field=models.TextField(blank=True, help_text="Si vide, le nom de l'entité sera utilisé", max_length=1024, verbose_name='Signature des emails'),
        ),
        migrations.AddField(
            model_name='permitrequest',
            name='additional_decision_information',
            field=models.TextField(blank=True, help_text='Facultative, sera transmise au requérant', max_length=2048, verbose_name='Information complémentaire'),
        ),
        migrations.AddField(
            model_name='worksobjectproperty',
            name='line_number_for_textarea',
            field=models.PositiveIntegerField(blank=True, default=1, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(50)], verbose_name='Nombre de lignes de la zone de texte'),
        ),
    ]
