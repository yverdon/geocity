# Generated by Django 3.1.4 on 2021-01-29 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('permits', '0016_fix_property_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermitRequestAmendProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='nom')),
                ('is_mandatory', models.BooleanField(default=False, verbose_name='obligatoire')),
                ('works_object_types', models.ManyToManyField(related_name='amend_properties', to='permits.WorksObjectType', verbose_name='objets des travaux')),
            ],
            options={
                'verbose_name': '2.2 Configuration de champ de traitement de demande',
                'verbose_name_plural': '2.2 Configuration des champs de traitement des demandes',
            },
        ),
        migrations.RemoveField(
            model_name='historicalpermitrequest',
            name='archeology_status',
        ),
        migrations.RemoveField(
            model_name='historicalpermitrequest',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='historicalpermitrequest',
            name='exemption',
        ),
        migrations.RemoveField(
            model_name='historicalpermitrequest',
            name='opposition',
        ),
        migrations.RemoveField(
            model_name='historicalpermitrequest',
            name='price',
        ),
        migrations.RemoveField(
            model_name='permitrequest',
            name='archeology_status',
        ),
        migrations.RemoveField(
            model_name='permitrequest',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='permitrequest',
            name='exemption',
        ),
        migrations.RemoveField(
            model_name='permitrequest',
            name='opposition',
        ),
        migrations.RemoveField(
            model_name='permitrequest',
            name='price',
        ),
        migrations.CreateModel(
            name='HistoricalPermitRequestAmendPropertyValue',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('value', models.TextField(blank=True, verbose_name='traitement info')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('property', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='permits.permitrequestamendproperty', verbose_name='caractéristique')),
                ('works_object_type_choice', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='permits.worksobjecttypechoice', verbose_name='objet des travaux')),
            ],
            options={
                'verbose_name': 'historical permit request amend property value',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='PermitRequestAmendPropertyValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(blank=True, verbose_name='traitement info')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='permits.permitrequestamendproperty', verbose_name='caractéristique')),
                ('works_object_type_choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amend_properties', to='permits.worksobjecttypechoice', verbose_name='objet des travaux')),
            ],
            options={
                'unique_together': {('property', 'works_object_type_choice')},
            },
        ),
    ]
