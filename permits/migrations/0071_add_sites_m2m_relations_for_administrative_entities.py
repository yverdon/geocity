# Generated by Django 3.2.12 on 2022-04-13 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("permits", "0070_publish_fields_for_public_permitrequests"),
    ]

    operations = [
        migrations.AddField(
            model_name="permitadministrativeentity",
            name="sites",
            field=models.ManyToManyField(to="sites.Site"),
        ),
    ]