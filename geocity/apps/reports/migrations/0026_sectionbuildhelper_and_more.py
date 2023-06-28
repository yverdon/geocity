# Generated by Django 4.2.1 on 2023-06-19 07:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0025_rename_api_price_field"),
    ]

    operations = [
        migrations.CreateModel(
            name="SectionBuildHelper",
            fields=[
                (
                    "section_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="reports.section",
                    ),
                ),
            ],
            options={
                "verbose_name": "Aide",
            },
            bases=("reports.section",),
        ),
        migrations.RemoveField(
            model_name="sectionamendproperty",
            name="show_form_name",
        ),
        migrations.RemoveField(
            model_name="sectiondetail",
            name="show_form_name",
        ),
        migrations.AddField(
            model_name="sectionamendproperty",
            name="form_name",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, "Aucun"),
                    (1, "Formulaire"),
                    (2, "Catégorie"),
                    (3, "Formulaire (Catégorie)"),
                ],
                default=3,
                help_text="Choix de la valeur à afficher pour le nom du formulaire",
                verbose_name="Affichage du nom du formulaire",
            ),
        ),
        migrations.AddField(
            model_name="sectiondetail",
            name="form_name",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, "Aucun"),
                    (1, "Formulaire"),
                    (2, "Catégorie"),
                    (3, "Formulaire (Catégorie)"),
                ],
                default=3,
                help_text="Choix de la valeur à afficher pour le nom du formulaire",
                verbose_name="Affichage du nom du formulaire",
            ),
        ),
    ]
