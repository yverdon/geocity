# Generated by Django 4.2.7 on 2023-12-11 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0026_form_max_submissions_bypass_enabled_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="field",
            name="is_public_when_permitrequest_is_public",
        ),
        migrations.AddField(
            model_name="field",
            name="api_light",
            field=models.BooleanField(
                default=False,
                help_text="Lorsque cette case est cochée, ce champ est affiché dans la version light de l'api (/rest/RESSOURCE) <b>si la demande est rendue publique par le pilote</b>.<br>\n            Afin de ne pas afficher trop d'informations, le champ est masqué pour améliorer la rapidité de l'API.<br>\n            Pour afficher la version normale de l'api, il faut se rendre sur une seule ressource (/rest/RESSOURCE/:ID).",
                verbose_name="Visible dans l'API light",
            ),
        ),
        migrations.AddField(
            model_name="field",
            name="filter_for_api",
            field=models.BooleanField(
                default=False,
                help_text="Lorsque cette case est cochée, ce champ peut être utilisé pour filtrer <b>si la demande est rendue publique par le pilote</b>.<br>\n            Actuellement ne fonctionne que pour les champs à choix simple ou multiples dans agenda.",
                verbose_name="Filtre pour API",
            ),
        ),
        migrations.AddField(
            model_name="field",
            name="public_if_submission_public",
            field=models.BooleanField(
                default=False,
                help_text="Lorsque cette case est cochée, ce champ est affiché <b>si la demande est rendue publique par le pilote</b>.<br>\n            Actuellement utilisé pour l'application geocalendrier et agenda",
                verbose_name="Information publique",
            ),
        ),
        migrations.AddField(
            model_name="form",
            name="agenda_visible",
            field=models.BooleanField(
                default=False,
                help_text="Lorsque cette case est cochée, les données de ce formulaire sont accessibles dans l'API <b>/rest/agenda/ si la demande est rendue publique par le pilote</b><br>\n            Le pilote peut alors contrôler la publication dans l'agenda dans l'onglet traitement",
                verbose_name="Visible dans l'agenda",
            ),
        ),
    ]
