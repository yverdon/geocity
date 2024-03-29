# Generated by Django 3.2.15 on 2022-11-10 14:25

from django.db import migrations


def rename_report_sections_variables(apps, schema_editor):
    SectionParagraph = apps.get_model("reports", "SectionParagraph")

    for section in SectionParagraph.objects.all():
        section.content = section.content.replace(
            "permit_request_works_object_types_names", "submission_forms_names"
        )
        section.content = section.content.replace("wot_data", "form_data")
        section.save()


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0012_report_document_types"),
    ]

    operations = [migrations.RunPython(rename_report_sections_variables)]
