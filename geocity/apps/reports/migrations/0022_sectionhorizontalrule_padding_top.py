# Generated by Django 4.1.7 on 2023-03-23 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0021_remove_section_padding_top_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="sectionhorizontalrule",
            name="padding_top",
            field=models.PositiveIntegerField(
                default=0,
                help_text="Espace vide au dessus afin de placer le texte au bon endroit (en pixels). Augmenter la valeur fait descendre le texte",
                verbose_name="Espace vide au dessus",
            ),
        ),
    ]