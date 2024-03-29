# Generated by Django 4.2.9 on 2024-01-24 08:20

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("accounts", "0017_service_fee"),
        (
            "submissions",
            "0025_alter_historicalpostfinancetransaction_authorization_timeout_on_and_more",
        ),
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
                    ("can_manage_service_fee", "Gérer une prestation"),
                ],
                "verbose_name": "2.2 Consultation de la demande",
                "verbose_name_plural": "2.2 Consultation des demandes",
            },
        ),
        migrations.AddField(
            model_name="historicalsubmission",
            name="service_fees_total_price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default=0.0,
                help_text="Le montant total des prestations effectuées pour cette demande. ",
                max_digits=12,
                null=True,
                verbose_name="Montant total des prestations [CHF]",
            ),
        ),
        migrations.AddField(
            model_name="submission",
            name="service_fees_total_price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default=0.0,
                help_text="Le montant total des prestations effectuées pour cette demande. ",
                max_digits=12,
                null=True,
                verbose_name="Montant total des prestations [CHF]",
            ),
        ),
        migrations.CreateModel(
            name="ServiceFeeType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Prestation")),
                (
                    "fix_price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=None,
                        help_text="Le tarif forfaitaire de cette prestation.",
                        max_digits=12,
                        null=True,
                        verbose_name="Tarif forfaitaire [CHF]",
                    ),
                ),
                (
                    "fix_price_editable",
                    models.BooleanField(
                        default=False,
                        help_text="Exemple: montant demandant un calcul spécifique à réaliser en dehors de l'application",
                        verbose_name="Montant à saisir manuelllement",
                    ),
                ),
                (
                    "is_visible_by_validator",
                    models.BooleanField(
                        default=False,
                        help_text="Est visible par le validateur",
                        verbose_name="Visible par le validateur",
                    ),
                ),
                (
                    "administrative_entity",
                    models.ForeignKey(
                        help_text="Entité administrative.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="administrative_entity",
                        to="accounts.administrativeentity",
                        verbose_name="Entité administrative",
                    ),
                ),
            ],
            options={
                "verbose_name": "2.4 Type de prestation",
                "verbose_name_plural": "2.4 Types de prestation",
            },
        ),
        migrations.CreateModel(
            name="ServiceFee",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Date de création."
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Date de dernière modification."
                    ),
                ),
                (
                    "provided_at",
                    models.DateField(
                        default=django.utils.timezone.now,
                        help_text="La prestation a été saisie à cette date.",
                        verbose_name="Saisie le",
                    ),
                ),
                (
                    "time_spent_on_task",
                    models.DurationField(
                        default=0,
                        help_text="Temps passé pour effectuer la prestation (en minutes).",
                        null=True,
                        verbose_name="Durée [m]",
                    ),
                ),
                (
                    "hourly_rate",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        help_text="Le tarif horaire de la prestation. Choisi par l'intégrateur.",
                        max_digits=12,
                        null=True,
                        verbose_name="Tarif horaire [CHF]",
                    ),
                ),
                (
                    "monetary_amount",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        help_text="Le montant de la prestation. Calulé automatiquement en fonction du tarif horaire. Est fixe si la prestation est forfaitaire. Certains montants fixes peuvent être modifiables lorsque le type de prestation exige un calcul spécifique. ",
                        max_digits=12,
                        verbose_name="Montant [CHF]",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        help_text="La prestation a été créé par cet utilisateur.",
                        max_length=255,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="service_fee_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Créée par",
                    ),
                ),
                (
                    "permit_department",
                    models.ForeignKey(
                        help_text="Département.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="permit_department",
                        to="accounts.permitdepartment",
                        verbose_name="Département",
                    ),
                ),
                (
                    "provided_by",
                    models.ForeignKey(
                        help_text="La prestation a été effectuée au nom de cet utilisateur.",
                        max_length=255,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="service_fee_provided_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Saisie par",
                    ),
                ),
                (
                    "service_fee_type",
                    models.ForeignKey(
                        help_text="Choix de la prestation ; à effectuer dans une liste prédéfinie.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="service_fee_type",
                        to="submissions.servicefeetype",
                        verbose_name="Type de prestation",
                    ),
                ),
                (
                    "submission",
                    models.ForeignKey(
                        help_text="Demande",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="service_fee",
                        to="submissions.submission",
                        verbose_name="Demande",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        help_text="La prestation a été mise à jour par cet utilisateur.",
                        max_length=255,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="service_fee_updated_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Mise à jour par",
                    ),
                ),
            ],
        ),
    ]
