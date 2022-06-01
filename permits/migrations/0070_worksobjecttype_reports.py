# Generated by Django 3.2.13 on 2022-06-01 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
        ('permits', '0069_rename_short_name_and_is_public_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksobjecttype',
            name='reports',
            field=models.ManyToManyField(related_name='worksobjecttypes', to='reports.Report'),
        ),
    ]
