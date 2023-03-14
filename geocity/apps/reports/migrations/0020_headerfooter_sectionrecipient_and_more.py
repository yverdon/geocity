# Generated by Django 4.1.7 on 2023-03-02 14:12

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import geocity.apps.reports.fields
import geocity.apps.reports.models
import geocity.fields


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        (
            "reports",
            "0019_alter_complementarydocumenttypeforadminsite_options_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="HeaderFooter",
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
                    "page",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Toutes les pages"),
                            (1, "Première page"),
                            (2, "Toutes sauf la première page"),
                        ],
                        default=0,
                        help_text="Choix des pages auxquelles doit s'appliquer l'en-tête et pied de page",
                        verbose_name="Page",
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        choices=[
                            ("@bottom-center", "Pied de page - Centre"),
                            ("@bottom-left", "Pied de page - Gauche"),
                            ("@bottom-left-corner", "Pied de page - Coin gauche"),
                            ("@bottom-right", "Pied de page - Droite"),
                            ("@bottom-right-corner", "Pied de page - Coin Droite"),
                            ("@left-bottom", "Bordure gauche - Bas de page"),
                            ("@left-middle", "Bordure gauche - Milieu de page"),
                            ("@left-top", "Bordure gauche - Haut de page"),
                            ("@right-bottom", "Bordure droite - Bas de page"),
                            ("@right-middle", "Bordure droite - Milieu de page"),
                            ("@right-top", "Bordure droite - Haut de page"),
                            ("@top-center", "En-tête - Centre"),
                            ("@top-left", "En-tête - Gauche"),
                            ("@top-left-corner", "En-tête - Coin gauche"),
                            ("@top-right", "En-tête - Droite"),
                            ("@top-right-corner", "En-tête - Coin Droite"),
                        ],
                        default="@bottom-center",
                        max_length=255,
                        verbose_name="Emplacement",
                    ),
                ),
                (
                    "polymorphic_ctype",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="polymorphic_%(app_label)s.%(class)s_set+",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=geocity.apps.reports.models.NON_POLYMORPHIC_CASCADE,
                        related_name="header_footers",
                        to="reports.report",
                    ),
                ),
            ],
            options={
                "verbose_name": "En-tête et pied de page",
                "verbose_name_plural": "En-têtes et pieds de page",
            },
        ),
        migrations.CreateModel(
            name="SectionRecipient",
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
                (
                    "is_recommended",
                    models.BooleanField(
                        default=False,
                        help_text='Ajoute le texte "RECOMMANDEE" en première ligne',
                        verbose_name="Recommandée",
                    ),
                ),
            ],
            options={
                "verbose_name": "Destinataire",
            },
            bases=("reports.section",),
        ),
        migrations.RemoveField(
            model_name="reportlayout",
            name="font",
        ),
        migrations.AddField(
            model_name="reportlayout",
            name="font_family",
            field=models.CharField(
                blank=True,
                default="Roboto",
                help_text='La liste des polices disponibles est visible sur <a href="https://fonts.google.com/" target="_blank">Google Fonts</a>',
                max_length=1024,
                null=True,
                verbose_name="Police",
            ),
        ),
        migrations.AddField(
            model_name="reportlayout",
            name="font_size_header_footer",
            field=models.PositiveIntegerField(
                default=11,
                help_text="Taille de la police (en pixels). S'applique à tous les en-tête et pieds de page",
                verbose_name="Taille de la police en-tête et pied de page",
            ),
        ),
        migrations.AddField(
            model_name="reportlayout",
            name="font_size_section",
            field=models.PositiveIntegerField(
                default=12,
                help_text="Taille de la police (en pixels). S'applique à tous les paragraphes",
                verbose_name="Taille de la police",
            ),
        ),
        migrations.AddField(
            model_name="section",
            name="is_new_page",
            field=models.BooleanField(
                default=False,
                help_text="Commencer cette section sur une nouvelle page ?",
                verbose_name="Nouvelle page",
            ),
        ),
        migrations.AddField(
            model_name="section",
            name="padding_top",
            field=models.PositiveIntegerField(
                default=0,
                help_text="Espace vide au dessus afin de placer le texte au bon endroit (en pixels). Augmenter la valeur fait descendre le texte",
                verbose_name="Espace vide au dessus",
            ),
        ),
        migrations.AddField(
            model_name="sectionamendproperty",
            name="title",
            field=models.CharField(
                blank=True,
                default="Commentaire·s du secrétariat",
                max_length=2000,
                verbose_name="Titre",
            ),
        ),
        migrations.AddField(
            model_name="sectionamendproperty",
            name="title_size",
            field=models.CharField(
                choices=[
                    ("h1", "Titre 1"),
                    ("h2", "Titre 2"),
                    ("h3", "Titre 3"),
                    ("h4", "Titre 4"),
                    ("h5", "Titre 5"),
                    ("h6", "Titre 6"),
                ],
                default="h2",
                help_text="S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite",
                max_length=255,
                verbose_name="Taille des titres",
            ),
        ),
        migrations.AddField(
            model_name="sectionauthor",
            name="title",
            field=models.CharField(
                blank=True,
                default="Auteur·e de la demande",
                max_length=2000,
                verbose_name="Titre",
            ),
        ),
        migrations.AddField(
            model_name="sectionauthor",
            name="title_size",
            field=models.CharField(
                choices=[
                    ("h1", "Titre 1"),
                    ("h2", "Titre 2"),
                    ("h3", "Titre 3"),
                    ("h4", "Titre 4"),
                    ("h5", "Titre 5"),
                    ("h6", "Titre 6"),
                ],
                default="h2",
                help_text="S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite",
                max_length=255,
                verbose_name="Taille des titres",
            ),
        ),
        migrations.AddField(
            model_name="sectioncontact",
            name="title",
            field=models.CharField(
                blank=True, default="Contact·s", max_length=2000, verbose_name="Titre"
            ),
        ),
        migrations.AddField(
            model_name="sectioncontact",
            name="title_size",
            field=models.CharField(
                choices=[
                    ("h1", "Titre 1"),
                    ("h2", "Titre 2"),
                    ("h3", "Titre 3"),
                    ("h4", "Titre 4"),
                    ("h5", "Titre 5"),
                    ("h6", "Titre 6"),
                ],
                default="h2",
                help_text="S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite",
                max_length=255,
                verbose_name="Taille des titres",
            ),
        ),
        migrations.AddField(
            model_name="sectioncreditor",
            name="title",
            field=models.CharField(
                blank=True,
                default="Adresse de facturation",
                max_length=2000,
                verbose_name="Titre",
            ),
        ),
        migrations.AddField(
            model_name="sectioncreditor",
            name="title_size",
            field=models.CharField(
                choices=[
                    ("h1", "Titre 1"),
                    ("h2", "Titre 2"),
                    ("h3", "Titre 3"),
                    ("h4", "Titre 4"),
                    ("h5", "Titre 5"),
                    ("h6", "Titre 6"),
                ],
                default="h2",
                help_text="S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite",
                max_length=255,
                verbose_name="Taille des titres",
            ),
        ),
        migrations.AddField(
            model_name="sectiondetail",
            name="line_height",
            field=models.PositiveSmallIntegerField(
                blank=True,
                default=12,
                help_text="Espace (en pixels) entre deux détails",
                null=True,
                verbose_name="Interligne",
            ),
        ),
        migrations.AddField(
            model_name="sectiondetail",
            name="show_form_name",
            field=models.BooleanField(
                default=True,
                help_text="Cocher cette option affiche le nom du formulaire (objet et type de demande)",
                verbose_name="Afficher le nom du formulaire",
            ),
        ),
        migrations.AddField(
            model_name="sectiondetail",
            name="style",
            field=models.PositiveSmallIntegerField(
                choices=[(0, "champ : valeur"), (1, "champ (tab) valeur")],
                default=0,
                help_text="Choisir le style d'affichage",
                verbose_name="Style",
            ),
        ),
        migrations.AddField(
            model_name="sectiondetail",
            name="title",
            field=models.CharField(
                blank=True,
                default="Propriété·s de la demande",
                max_length=2000,
                verbose_name="Titre",
            ),
        ),
        migrations.AddField(
            model_name="sectiondetail",
            name="title_size",
            field=models.CharField(
                choices=[
                    ("h1", "Titre 1"),
                    ("h2", "Titre 2"),
                    ("h3", "Titre 3"),
                    ("h4", "Titre 4"),
                    ("h5", "Titre 5"),
                    ("h6", "Titre 6"),
                ],
                default="h2",
                help_text="S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite",
                max_length=255,
                verbose_name="Taille des titres",
            ),
        ),
        migrations.AddField(
            model_name="sectiondetail",
            name="undesired_properties",
            field=models.CharField(
                blank=True,
                help_text="Liste de champs à masquer, séparés par des points virgules ';' correspondant aux titre des champs (ex: hauteur;largeur)",
                max_length=2000,
                null=True,
                verbose_name="Nom de champs a masquer",
            ),
        ),
        migrations.AddField(
            model_name="sectionmap",
            name="title",
            field=models.CharField(
                blank=True,
                default="Localisation·s",
                max_length=2000,
                verbose_name="Titre",
            ),
        ),
        migrations.AddField(
            model_name="sectionmap",
            name="title_size",
            field=models.CharField(
                choices=[
                    ("h1", "Titre 1"),
                    ("h2", "Titre 2"),
                    ("h3", "Titre 3"),
                    ("h4", "Titre 4"),
                    ("h5", "Titre 5"),
                    ("h6", "Titre 6"),
                ],
                default="h2",
                help_text="S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite",
                max_length=255,
                verbose_name="Taille des titres",
            ),
        ),
        migrations.AddField(
            model_name="sectionparagraph",
            name="location",
            field=models.CharField(
                choices=[
                    ("content", "Toute la largeur"),
                    ("left", "Gauche"),
                    ("right", "Droite"),
                ],
                default="content",
                max_length=255,
                verbose_name="Emplacement du bloc",
            ),
        ),
        migrations.AddField(
            model_name="sectionparagraph",
            name="text_align",
            field=models.CharField(
                choices=[
                    ("left", "Gauche"),
                    ("right", "Droite"),
                    ("center", "Centre"),
                    ("justify", "Justifié"),
                ],
                default="justify",
                max_length=255,
                verbose_name="Alignement du texte",
            ),
        ),
        migrations.AddField(
            model_name="sectionparagraph",
            name="title_size",
            field=models.CharField(
                choices=[
                    ("h1", "Titre 1"),
                    ("h2", "Titre 2"),
                    ("h3", "Titre 3"),
                    ("h4", "Titre 4"),
                    ("h5", "Titre 5"),
                    ("h6", "Titre 6"),
                ],
                default="h2",
                help_text="S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite",
                max_length=255,
                verbose_name="Taille des titres",
            ),
        ),
        migrations.AddField(
            model_name="sectionplanning",
            name="title",
            field=models.CharField(
                blank=True, default="Planning", max_length=2000, verbose_name="Titre"
            ),
        ),
        migrations.AddField(
            model_name="sectionplanning",
            name="title_size",
            field=models.CharField(
                choices=[
                    ("h1", "Titre 1"),
                    ("h2", "Titre 2"),
                    ("h3", "Titre 3"),
                    ("h4", "Titre 4"),
                    ("h5", "Titre 5"),
                    ("h6", "Titre 6"),
                ],
                default="h2",
                help_text="S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite",
                max_length=255,
                verbose_name="Taille des titres",
            ),
        ),
        migrations.AddField(
            model_name="sectionstatus",
            name="title",
            field=models.CharField(
                blank=True,
                default="Statut de la demande",
                max_length=2000,
                verbose_name="Titre",
            ),
        ),
        migrations.AddField(
            model_name="sectionstatus",
            name="title_size",
            field=models.CharField(
                choices=[
                    ("h1", "Titre 1"),
                    ("h2", "Titre 2"),
                    ("h3", "Titre 3"),
                    ("h4", "Titre 4"),
                    ("h5", "Titre 5"),
                    ("h6", "Titre 6"),
                ],
                default="h2",
                help_text="S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite",
                max_length=255,
                verbose_name="Taille des titres",
            ),
        ),
        migrations.AddField(
            model_name="sectionvalidation",
            name="title",
            field=models.CharField(
                blank=True,
                default="Commentaire·s des services",
                max_length=2000,
                verbose_name="Titre",
            ),
        ),
        migrations.AddField(
            model_name="sectionvalidation",
            name="title_size",
            field=models.CharField(
                choices=[
                    ("h1", "Titre 1"),
                    ("h2", "Titre 2"),
                    ("h3", "Titre 3"),
                    ("h4", "Titre 4"),
                    ("h5", "Titre 5"),
                    ("h6", "Titre 6"),
                ],
                default="h2",
                help_text="S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite",
                max_length=255,
                verbose_name="Taille des titres",
            ),
        ),
        migrations.AlterField(
            model_name="reportlayout",
            name="background",
            field=geocity.apps.reports.fields.BackgroundFileField(
                blank=True,
                help_text="Image d'arrière plan (PNG).",
                null=True,
                storage=geocity.fields.PrivateFileSystemStorage(),
                upload_to="backgound_paper",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["png"]
                    )
                ],
                verbose_name="Papier à en-tête",
            ),
        ),
        migrations.AlterField(
            model_name="reportlayout",
            name="margin_bottom",
            field=models.PositiveIntegerField(default=15, verbose_name="Marge: bas"),
        ),
        migrations.AlterField(
            model_name="reportlayout",
            name="margin_left",
            field=models.PositiveIntegerField(default=15, verbose_name="Marge: gauche"),
        ),
        migrations.AlterField(
            model_name="reportlayout",
            name="margin_right",
            field=models.PositiveIntegerField(default=15, verbose_name="Marge: droite"),
        ),
        migrations.AlterField(
            model_name="reportlayout",
            name="margin_top",
            field=models.PositiveIntegerField(default=25, verbose_name="Marge: haut"),
        ),
        migrations.CreateModel(
            name="HeaderFooterDateTime",
            fields=[
                (
                    "headerfooter_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="reports.headerfooter",
                    ),
                ),
            ],
            options={
                "verbose_name": "Date et heure",
            },
            bases=("reports.headerfooter",),
        ),
        migrations.CreateModel(
            name="HeaderFooterLogo",
            fields=[
                (
                    "headerfooter_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="reports.headerfooter",
                    ),
                ),
                (
                    "logo",
                    geocity.apps.reports.fields.BackgroundFileField(
                        help_text="Image pour logo (PNG).",
                        storage=geocity.fields.PrivateFileSystemStorage(),
                        upload_to="backgound_paper",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["png"]
                            )
                        ],
                        verbose_name="Logo",
                    ),
                ),
                (
                    "logo_size",
                    models.PositiveIntegerField(
                        default=60,
                        help_text="Défini la taille de l'image en %. Choisir un nombre compris entre 0 et 100",
                        verbose_name="Taille",
                    ),
                ),
            ],
            options={
                "verbose_name": "Logo",
            },
            bases=("reports.headerfooter",),
        ),
        migrations.CreateModel(
            name="HeaderFooterPageNumber",
            fields=[
                (
                    "headerfooter_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="reports.headerfooter",
                    ),
                ),
            ],
            options={
                "verbose_name": "Numéro de page",
            },
            bases=("reports.headerfooter",),
        ),
        migrations.CreateModel(
            name="HeaderFooterParagraph",
            fields=[
                (
                    "headerfooter_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="reports.headerfooter",
                    ),
                ),
                (
                    "text_align",
                    models.CharField(
                        choices=[
                            ("left", "Gauche"),
                            ("right", "Droite"),
                            ("center", "Centre"),
                            ("justify", "Justifié"),
                        ],
                        default="left",
                        max_length=255,
                        verbose_name="Alignement du texte",
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        help_text="Texte à afficher",
                        max_length=1024,
                        verbose_name="Contenu",
                    ),
                ),
            ],
            options={
                "verbose_name": "Texte libre",
            },
            bases=("reports.headerfooter",),
        ),
        migrations.DeleteModel(
            name="SectionParagraphRight",
        ),
    ]
