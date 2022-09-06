# Generated by Django 3.2.15 on 2022-09-06 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('socialaccount', '0003_extra_data_default_dict'),
        ('sites', '0002_alter_domain_unique'),
        ('permits', '0079_add_iban_to_permitauthor_and_fix_typo'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('integrator', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group', verbose_name='Détails du Site')),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sites.site')),
            ],
            options={
                'verbose_name': '6.0 Configuration du site',
                'verbose_name_plural': '6.0 Configuration des sites',
            },
        ),
        migrations.AlterField(
            model_name='permitadministrativeentity',
            name='sites',
            field=models.ManyToManyField(related_name='administrative_entity', to='sites.Site', verbose_name='Détails du Site'),
        ),
        migrations.DeleteModel(
            name='Site',
        ),
    ]
