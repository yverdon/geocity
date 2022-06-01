# Generated by Django 3.2.13 on 2022-06-01 11:44

from django.db import migrations, models
import django.db.models.deletion
import streamfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportLayout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('width', models.PositiveIntegerField(default=210)),
                ('height', models.PositiveIntegerField(default=297)),
                ('margin_top', models.PositiveIntegerField(default=10)),
                ('margin_right', models.PositiveIntegerField(default=10)),
                ('margin_bottom', models.PositiveIntegerField(default=10)),
                ('margin_left', models.PositiveIntegerField(default=10)),
                ('font', models.CharField(blank=True, help_text='La liste des polices disponbiles est visible sur <a href="https://fonts.google.com/" target="_blank">Goole Fonts</a>', max_length=1024, null=True)),
                ('background', models.ImageField(blank=True, help_text='Image d\'arrière plan ("papier à en-tête")', null=True, upload_to='')),
            ],
            options={
                'verbose_name': "5.1 Configuration du modèle d'impression de rapport",
                'verbose_name_plural': "5.1 Configuration des modèles d'impression de rapport",
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('stream', streamfield.fields.StreamField(blank=True, default='[]')),
                ('layout', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='reports.reportlayout')),
            ],
            options={
                'verbose_name': '5.2 Configuration du rapport',
                'verbose_name_plural': '5.2 Configuration des rapports',
            },
        ),
    ]
