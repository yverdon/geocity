# Generated by Django 4.1.7 on 2023-04-03 11:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("accounts", "0011_add_signature_sheet_to_administrative_entity"),
        ("submissions", "0016_historicalsubmissionvalidation_comment_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="submission",
            options={
                "permissions": [
                    ("read_submission", "Consulter les demandes"),
                    ("amend_submission", "Traiter les demandes"),
                    ("edit_submission_validations", "Modifier les validations"),
                    ("validate_submission", "Valider les demandes"),
                    ("classify_submission", "Classer les demandes"),
                    ("edit_submission", "Modifier les demandes"),
                    ("view_private_form", "Voir les demandes restreintes"),
                    ("can_refund_transactions", "Rembourser une transaction"),
                    ("can_revert_refund_transactions", "Revenir sur un remboursement"),
                ],
                "verbose_name": "2.2 Consultation de la demande",
                "verbose_name_plural": "2.2 Consultation des demandes",
            },
        ),
        migrations.RemoveField(
            model_name="historicalsubmissionvalidation",
            name="comment_after",
        ),
        migrations.RemoveField(
            model_name="historicalsubmissionvalidation",
            name="comment_before",
        ),
        migrations.RemoveField(
            model_name="historicalsubmissionvalidation",
            name="comment_during",
        ),
        migrations.RemoveField(
            model_name="submissionvalidation",
            name="comment_after",
        ),
        migrations.RemoveField(
            model_name="submissionvalidation",
            name="comment_before",
        ),
        migrations.RemoveField(
            model_name="submissionvalidation",
            name="comment_during",
        ),
        migrations.AddField(
            model_name="historicalsubmissionvalidation",
            name="comment_is_visible_by_author",
            field=models.BooleanField(
                default=True,
                verbose_name="Commentaire visible par l'auteur de la demande",
            ),
        ),
        migrations.AddField(
            model_name="submissionvalidation",
            name="comment_is_visible_by_author",
            field=models.BooleanField(
                default=True,
                verbose_name="Commentaire visible par l'auteur de la demande",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubmissionvalidation",
            name="comment",
            field=models.TextField(blank=True, verbose_name="Commentaire"),
        ),
        migrations.AlterField(
            model_name="historicalsubmissionvalidation",
            name="department",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="accounts.permitdepartment",
                verbose_name="Département",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubmissionvalidation",
            name="validated_by",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Validé par",
            ),
        ),
        migrations.AlterField(
            model_name="submissionvalidation",
            name="comment",
            field=models.TextField(blank=True, verbose_name="Commentaire"),
        ),
        migrations.AlterField(
            model_name="submissionvalidation",
            name="department",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="submission_validations",
                to="accounts.permitdepartment",
                verbose_name="Département",
            ),
        ),
        migrations.AlterField(
            model_name="submissionvalidation",
            name="validated_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Validé par",
            ),
        ),
    ]
