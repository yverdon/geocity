# Generated by Django 4.1 on 2022-12-06 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("submissions", "0006_change_admin_order"),
        ("reports", "0015_alter_report_document_types_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ComplementaryDocumentTypeForAdminSite",
            fields=[],
            options={
                "verbose_name": "3.2 Catégorie de document",
                "verbose_name_plural": "3.2 Catégories de document",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("submissions.complementarydocumenttype",),
        ),
        migrations.AlterModelOptions(
            name="report",
            options={
                "permissions": [("can_generate_pdf", "Générer des documents pdf")],
                "verbose_name": "3.3 Modèle d'impression",
                "verbose_name_plural": "3.3 Modèles d'impression",
            },
        ),
    ]
