# Generated by Django 3.2.15 on 2022-09-06 12:26

from django.contrib.postgres.operations import TrigramExtension, UnaccentExtension
from django.db import migrations

from geocity import settings


def create_web_site(apps, schema_editor):

    Site = apps.get_model("sites", "Site")

    Site.objects.update_or_create(domain="web", name="web (internal calls)")


def update_site_data(apps, schema_editor):
    """
    Create default Site
    Fill SiteProfile data of Site
    Add default site to each PermitAdministrativeEntity
    """
    Site = apps.get_model("sites", "Site")
    SiteProfile = apps.get_model("accounts", "SiteProfile")
    PermitAdministrativeEntity = apps.get_model("accounts", "AdministrativeEntity")

    if not Site.objects.filter(domain=settings.DEFAULT_SITE).exists():
        Site.objects.get_or_create(domain=settings.DEFAULT_SITE, name="default site")

    default_site = Site.objects.get(domain=settings.DEFAULT_SITE)

    for entity in PermitAdministrativeEntity.objects.all():
        entity.sites.add(default_site)

    for site_obj in Site.objects.all():
        SiteProfile.objects.get_or_create(
            site=site_obj,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_merge_20221212_1053"),
    ]

    operations = [
        migrations.RunPython(update_site_data),
        migrations.RunPython(create_web_site),
        TrigramExtension(),
        UnaccentExtension(),
    ]