from django.db import migrations


def create_web_site(apps, schema_editor):

    Site = apps.get_model("sites", "Site")

    Site.objects.update_or_create(domain="web", name="web (internal calls)")


class Migration(migrations.Migration):

    dependencies = [
        ("permits", "0077_adapt_document_models"),
    ]

    operations = [migrations.RunPython(create_web_site)]
