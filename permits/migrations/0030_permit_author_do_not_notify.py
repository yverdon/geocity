# Generated by Django 3.2.4 on 2021-07-15 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permits', '0029_visibility_of_secreatariat_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpermitauthor',
            name='do_not_notify',
            field=models.BooleanField(default=False, verbose_name='ne pas me notifier'),
        ),
        migrations.AddField(
            model_name='permitauthor',
            name='do_not_notify',
            field=models.BooleanField(default=False, verbose_name='ne pas me notifier'),
        ),
    ]
