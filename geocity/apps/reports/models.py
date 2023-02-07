import base64
import re
from datetime import timedelta

from bs4 import BeautifulSoup
from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.staticfiles import finders
from django.core.files import File
from django.core.validators import FileExtensionValidator
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from jinja2.sandbox import SandboxedEnvironment
from knox.models import AuthToken
from polymorphic.models import PolymorphicModel

from geocity.apps.accounts.fields import AdministrativeEntityFileField
from geocity.apps.accounts.models import AdministrativeEntity

from .fields import BackgroundFileField
from .utils import DockerRunFailedError, run_docker_container


class ReportLayout(models.Model):
    """Page size/background/marings/fonts/etc, used by reports"""

    name = models.CharField(_("Nom"), max_length=150)
    width = models.PositiveIntegerField(_("Largeur"), default=210)
    height = models.PositiveIntegerField(_("Hauteur"), default=297)
    margin_top = models.PositiveIntegerField(_("Marge: haut"), default=25)
    margin_right = models.PositiveIntegerField(_("Marge: droite"), default=15)
    margin_bottom = models.PositiveIntegerField(_("Marge: bas"), default=15)
    margin_left = models.PositiveIntegerField(_("Marge: gauche"), default=15)
    font_family = models.CharField(
        _("Police"),
        max_length=1024,
        blank=True,
        null=True,
        help_text=_(
            'La liste des polices disponibles est visible sur <a href="https://fonts.google.com/" target="_blank">Google Fonts</a>'
        ),
    )
    font_size_section = models.PositiveIntegerField(
        _("Taille de la police des paragraphes"),
        default=12,
        help_text=_(
            "Taille de la police (en pixels). S'applique à tous les paragraphes"
        ),
    )
    font_size_style = models.PositiveIntegerField(
        _("Taille de la police des style"),
        default=11,
        help_text=_(
            "Taille de la police (en pixels). S'applique à tous les style (en-tête, pied de page et bordures)"
        ),
    )

    class Meta:
        verbose_name = _("3.1 Format de papier")
        verbose_name_plural = _("3.1 Formats de papier")

    background = BackgroundFileField(
        _("Papier à entête"),
        null=True,
        blank=True,
        upload_to="backgound_paper",
        help_text=_("Image d'arrière plan (PNG ou SVG)."),
        validators=[FileExtensionValidator(allowed_extensions=["svg", "png"])],
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
        limit_choices_to={"permit_department__is_integrator_admin": True},
    )

    class Meta:
        verbose_name = _("3.1 Format de papier")
        verbose_name_plural = _("3.1 Formats de papier")

    def __str__(self):
        return self.name


class Report(models.Model):
    """Report definition, allowing to generate reports for submissions"""

    class Meta:
        permissions = [
            ("can_generate_pdf", _("Générer des documents pdf")),
        ]
        verbose_name = _("3.3 Modèle d'impression")
        verbose_name_plural = _("3.3 Modèles d'impression")

    name = models.CharField(_("Nom"), max_length=150)
    layout = models.ForeignKey(
        ReportLayout,
        on_delete=models.RESTRICT,
        verbose_name=_("Format de papier"),
    )
    # reverse relationship is manually defined on submissions.ComplementaryDocumentType so it shows up on both sides in admin
    document_types = models.ManyToManyField(
        "submissions.ComplementaryDocumentType",
        blank=True,
        related_name="+",
        verbose_name=_("Types de documents"),
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
        limit_choices_to={"permit_department__is_integrator_admin": True},
    )
    is_visible = models.BooleanField(
        _("Visible"),
        default=True,
        help_text=_(
            "Rendre le modèle visible dans la liste des documents et impressions (décocher pour les modèles de confirmation / remboursement de paiement)"
        ),
    )

    def __str__(self):
        return self.name

    def create_default_report(administrative_entity_id):
        administrative_entity = get_object_or_404(
            AdministrativeEntity, pk=administrative_entity_id
        )

        name = "default " + administrative_entity.name

        layout, created = ReportLayout.objects.get_or_create(
            name=name,
            margin_top=25,
            margin_right=15,
            margin_bottom=15,
            margin_left=15,
            integrator=administrative_entity.integrator,
        )

        _bg_path = finders.find("reports/report-letter-paper-template.png")
        background_image = open(_bg_path, "rb")
        layout.background.save(
            "report-letter-paper.png", File(background_image), save=True
        )
        layout.save()

        report, created = Report.objects.get_or_create(
            name=name,
            layout=layout,
            integrator=administrative_entity.integrator,
        )

        SectionParagraph.objects.get_or_create(
            order=1,
            report=report,
            title="Example report",
            content="<p>This is an example report. It could be an approval, or any type of report related to a request.</p>",
        )

        SectionParagraph.objects.get_or_create(
            order=2,
            report=report,
            title="Demand summary",
            content="<p>This demand contains the following objects.</p><ul>{% for form in request_data.properties.submission_forms_names.values() %}<li>{{form}}</li>{% endfor %}</ul>",
        )

        SectionParagraph.objects.get_or_create(
            order=3,
            report=report,
            title="Raw request data",
            content="<pre>{{request_data}}</pre>",
        )

        SectionParagraph.objects.get_or_create(
            order=4,
            report=report,
            title="Raw form data",
            content="<pre>{{form_data}}</pre>",
        )

        SectionMap.objects.get_or_create(
            order=5,
            report=report,
        )

        SectionAuthor.objects.get_or_create(
            order=6,
            report=report,
        )

        return name, created


# https://github.com/django-polymorphic/django-polymorphic/issues/229#issuecomment-398434412
def NON_POLYMORPHIC_CASCADE(collector, field, sub_objs, using):
    return models.CASCADE(collector, field, sub_objs.non_polymorphic(), using)


class heading(models.TextChoices):
    H1 = "h1", _("h1")
    H2 = "h2", _("h2")
    H3 = "h3", _("h3")
    H4 = "h4", _("h4")
    H5 = "h5", _("h5")
    H6 = "h6", _("h6")


class Section(PolymorphicModel):
    class Meta:
        verbose_name = _("Paragraphe")
        verbose_name_plural = _("Paragraphes")
        ordering = ["order"]

    report = models.ForeignKey(
        Report, on_delete=NON_POLYMORPHIC_CASCADE, related_name="sections"
    )
    order = models.PositiveIntegerField(_("Ordre du paragraphe"), null=True, blank=True)
    padding_top = models.PositiveIntegerField(
        _("Espace vide au dessus"),
        default=0,
        help_text=_(
            "Espace vide au dessus afin de placer le texte au bon endroit (en pixels). Augmenter la valeur fait descendre le texte"
        ),
    )
    is_new_page = models.BooleanField(
        _("Nouvelle page"),
        default=False,
        help_text=_("Commencer cette section sur une nouvelle page ?"),
    )

    def prepare_context(self, request, base_context):
        """Subclass this to add elements to the context (make sure to return a copy if you change it)"""
        return {
            **base_context,
            "section": self,
            "settings": settings,
        }

    @property
    def css_class(self):
        return re.sub("^Section", "section-", self.__class__.__name__).lower()

    def __str__(self):
        return self._meta.verbose_name


class SectionMap(Section):
    title = models.CharField(
        _("Titre"), default="Localisation·s", blank=True, max_length=2000
    )
    title_size = models.CharField(
        _("Taille des titres"),
        choices=heading.choices,
        default=heading.H2,
        max_length=255,
        help_text=_(
            "S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite"
        ),
    )
    qgis_project_file = AdministrativeEntityFileField(
        _("Projet QGIS '*.qgs'"),
        validators=[FileExtensionValidator(allowed_extensions=["qgs"])],
        upload_to="qgis_templates",
        blank=True,
        help_text=(
            _("Si aucun projet n'est ajouté, le projet par défaut sera utilisé.")
        ),
    )
    qgis_print_template_name = models.CharField(
        _("Nom du modèle QGIS"),
        max_length=30,
        blank=True,
        default="paysage-cadastre",
        help_text=(_("Modèles du projet par défaut: paysage-cadastre, paysage-ortho")),
    )

    class Meta:
        verbose_name = _("Carte")

    def get_context(self, context):
        context = super().get_context(context)

    def _generate_image(self, request, base_context):

        # Generate a token
        authtoken, token = AuthToken.objects.create(
            request.user, expiry=timedelta(minutes=5)
        )

        # Create a docker container to generate the image
        commands = [
            "/io/project.qgs",
            "/io/output.png",
            self.qgis_print_template_name,
            str(base_context["submission"].id),
            str(token),
            ",".join(settings.ALLOWED_HOSTS),
        ]

        try:
            output = run_docker_container(
                "geocity_qgis",
                commands,
                file_input=("/io/project.qgs", self.qgis_project_file.file),
                file_output="/io/output.png",
            )
        except DockerRunFailedError:
            # Return error image
            path = finders.find("reports/error.png")
            output = open(path, "rb")

        authtoken.delete()

        # Prepare the dataurl
        data = base64.b64encode(output.read()).decode("ascii")
        return f"data:image/png;base64,{data}"

    def prepare_context(self, request, base_context):
        # Return updated context
        return {
            **super().prepare_context(request, base_context),
            "map_data_url": self._generate_image(request, base_context),
        }

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Upload a default project if none is provided
        if not self.qgis_project_file:
            # Open an existing file using Python's built-in open()
            _qgis_path = finders.find("reports/report-template.qgs")
            qgis_template_project = File(open(_qgis_path, "rb"))
            self.qgis_project_file.save(
                "report-template-dev.qgs", File(qgis_template_project)
            )


class SectionParagraph(Section):
    title = models.CharField(_("Titre"), default="", blank=True, max_length=2000)
    title_size = models.CharField(
        _("Taille des titres"),
        choices=heading.choices,
        default=heading.H2,
        max_length=255,
        help_text=_(
            "S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite"
        ),
    )
    content = RichTextField(
        _("Contenu"),
        help_text=(
            _(
                'Il est possible d\'inclure des variables et de la logique avec la <a href="https://jinja.palletsprojects.com/en/3.1.x/templates/">syntaxe Jinja</a>. Les variables de la demande sont accessible dans `{{request_data}}`, celles du formulaire dans `{{form_data}}`, celles des transactions dans `{{transaction_data}}`.'
            )
        ),
    )

    class Meta:
        verbose_name = _("Paragraphe libre")

    def _render_user_template(self, base_context):
        # User template have only access to pure json elements for security reasons
        inner_context = {
            # TODO rename to `submission_data` (& migrate sections) to match new naming
            "request_data": base_context["request_data"],
            "form_data": base_context["form_data"],
        }
        if "transaction_data" in base_context:
            inner_context["transaction_data"] = base_context["transaction_data"]

        env = SandboxedEnvironment()
        rendered_html = env.from_string(self.content).render(inner_context)
        return mark_safe(rendered_html)

    def prepare_context(self, request, base_context):
        # Return updated context
        return {
            **super().prepare_context(request, base_context),
            "rendered_content": self._render_user_template(base_context),
        }


class SectionParagraphRight(Section):
    title = models.CharField(_("Titre"), default="", blank=True, max_length=2000)
    title_size = models.CharField(
        _("Taille des titres"),
        choices=heading.choices,
        default=heading.H2,
        max_length=255,
        help_text=_(
            "S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite"
        ),
    )
    content = RichTextField(
        _("Contenu"),
        help_text=(
            _(
                'Il est possible d\'inclure des variables et de la logique avec la <a href="https://jinja.palletsprojects.com/en/3.1.x/templates/">syntaxe Jinja</a>. Les variables de la demande sont accessible dans `{{request_data}}`, celles du formulaire dans `{{form_data}}`, celles des transactions dans `{{transaction_data}}`.'
            )
        ),
    )

    class Meta:
        verbose_name = _("Paragraphe libre aligné à droite")

    def _render_user_template(self, base_context):
        # User template have only access to pure json elements for security reasons
        inner_context = {
            # TODO rename to `submission_data` (& migrate sections) to match new naming
            "request_data": base_context["request_data"],
            "form_data": base_context["form_data"],
        }
        if "transaction_data" in base_context:
            inner_context["transaction_data"] = base_context["transaction_data"]
        env = SandboxedEnvironment()
        rendered_html = env.from_string(self.content).render(inner_context)
        return mark_safe(rendered_html)

    def prepare_context(self, request, base_context):
        # Return updated context
        return {
            **super().prepare_context(request, base_context),
            "rendered_content": self._render_user_template(base_context),
        }


class SectionContact(Section):
    title = models.CharField(
        _("Titre"), default="Contact·s", blank=True, max_length=2000
    )
    title_size = models.CharField(
        _("Taille des titres"),
        choices=heading.choices,
        default=heading.H2,
        max_length=255,
        help_text=_(
            "S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite"
        ),
    )

    class Meta:
        verbose_name = _("Contact·s")


class SectionAuthor(Section):
    title = models.CharField(
        _("Titre"), default="Auteur·e de la demande", blank=True, max_length=2000
    )
    title_size = models.CharField(
        _("Taille des titres"),
        choices=heading.choices,
        default=heading.H2,
        max_length=255,
        help_text=_(
            "S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite"
        ),
    )

    class Meta:
        verbose_name = _("Auteur")


class SectionDetail(Section):
    title = models.CharField(
        _("Titre"), default="Propriété·s de la demande", blank=True, max_length=2000
    )
    title_size = models.CharField(
        _("Taille des titres"),
        choices=heading.choices,
        default=heading.H2,
        max_length=255,
        help_text=_(
            "S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite"
        ),
    )

    class Meta:
        verbose_name = _("Détail·s")


class SectionPlanning(Section):
    title = models.CharField(
        _("Titre"), default="Planning", blank=True, max_length=2000
    )
    title_size = models.CharField(
        _("Taille des titres"),
        choices=heading.choices,
        default=heading.H2,
        max_length=255,
        help_text=_(
            "S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite"
        ),
    )

    class Meta:
        verbose_name = _("Planning")


class SectionHorizontalRule(Section):
    class Meta:
        verbose_name = _("Ligne horizontale")


class SectionValidation(Section):
    title = models.CharField(
        _("Titre"), default="Commentaire·s des services", blank=True, max_length=2000
    )
    title_size = models.CharField(
        _("Taille des titres"),
        choices=heading.choices,
        default=heading.H2,
        max_length=255,
        help_text=_(
            "S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite"
        ),
    )

    class Meta:
        verbose_name = _("Commentaire·s des services")


class SectionAmendProperty(Section):
    title = models.CharField(
        _("Titre"), default="Commentaire·s du secrétariat", blank=True, max_length=2000
    )
    title_size = models.CharField(
        _("Taille des titres"),
        choices=heading.choices,
        default=heading.H2,
        max_length=255,
        help_text=_(
            "S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite"
        ),
    )

    class Meta:
        verbose_name = _("Commentaire·s du secrétariat")


class SectionStatus(Section):
    title = models.CharField(
        _("Titre"), default="Statut de la demande", blank=True, max_length=2000
    )
    title_size = models.CharField(
        _("Taille des titres"),
        choices=heading.choices,
        default=heading.H2,
        max_length=255,
        help_text=_(
            "S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite"
        ),
    )

    class Meta:
        verbose_name = _("Statut")


class SectionCreditor(Section):
    title = models.CharField(
        _("Titre"), default="Adresse de facturation", blank=True, max_length=2000
    )
    title_size = models.CharField(
        _("Taille des titres"),
        choices=heading.choices,
        default=heading.H2,
        max_length=255,
        help_text=_(
            "S'applique au titre des tous les paragraphes. h1 taille la plus grande, h6 la plus petite"
        ),
    )

    class Meta:
        verbose_name = _("Adresse de facturation")


class SectionMailing(Section):
    padding_top = None
    is_recommended = models.BooleanField(
        _("Recommandée"),
        default=False,
        help_text=_('Ajoute le texte "RECOMMANDEE" en première ligne'),
    )
    padding_top_mailing = models.PositiveIntegerField(
        _("Espace vide au dessus"),
        default=20,
        help_text=_(
            "Espace vide au dessus afin de placer le texte au bon endroit (en pixels). Augmenter la valeur fait descendre le texte"
        ),
    )

    class Meta:
        verbose_name = _("Publipostage")


class Style(PolymorphicModel):
    class Location(models.TextChoices):
        BOTTOM_CENTER = "@bottom-center", _("Pied de page - Centre")
        BOTTOM_LEFT = "@bottom-left", _("Pied de page - Gauche")
        BOTTOM_LEFT_CORNER = "@bottom-left-corner", _("Pied de page - Coin gauche")
        BOTTOM_RIGHT = "@bottom-right", _("Pied de page - Droite")
        BOTTOM_RIGHT_CORNER = "@bottom-right-corner", _("Pied de page - Coin Droite")
        LEFT_BOTTOM = "@left-bottom", _("Bordure gauche - Bas de page")
        LEFT_MIDDLE = "@left-middle", _("Bordure gauche - Milieu de page")
        LEFT_TOP = "@left-top", _("Bordure gauche - Haut de page")
        RIGHT_BOTTOM = "@right-bottom", _("Bordure droite - Bas de page")
        RIGHT_MIDDLE = "@right-middle", _("Bordure droite - Milieu de page")
        RIGHT_TOP = "@right-top", _("Bordure droite - Haut de page")
        TOP_CENTER = "@top-center", _("En-tête - Centre")
        TOP_LEFT = "@top-left", _("En-tête - Gauche")
        TOP_LEFT_CORNER = "@top-left-corner", _("En-tête - Coin gauche")
        TOP_RIGHT = "@top-right", _("En-tête - Droite")
        TOP_RIGHT_CORNER = "@top-right-corner", _("En-tête - Coin Droite")

    ALL_PAGES = 0
    FIRST_PAGE = 1
    NOT_FIRST_PAGE = 2

    PAGES = (
        (ALL_PAGES, _("Toutes les pages")),
        (FIRST_PAGE, _("Première page")),
        (NOT_FIRST_PAGE, _("Toutes sauf la première page")),
    )

    report = models.ForeignKey(
        Report, on_delete=NON_POLYMORPHIC_CASCADE, related_name="styles"
    )
    page = models.PositiveSmallIntegerField(
        _("Page"),
        choices=PAGES,
        default=ALL_PAGES,
        help_text=_("Choix des pages auxquelles doit s'appliquer le style"),
    )
    location = models.CharField(
        _("Emplacement"),
        choices=Location.choices,
        default=Location.BOTTOM_CENTER,
        max_length=255,
    )

    def prepare_context(self, request, base_context):
        """Subclass this to add elements to the context (make sure to return a copy if you change it)"""
        return {
            **base_context,
            "style": self,
            "settings": settings,
        }

    class Meta:
        verbose_name = _("Style")
        verbose_name_plural = _("Styles")

    @property
    def css_class(self):
        return re.sub("^Style", "style-", self.__class__.__name__).lower()

    def __str__(self):
        return self._meta.verbose_name


class StylePageNumber(Style):
    class Meta:
        verbose_name = _("Numéro de page")


class StyleDateTime(Style):
    class Meta:
        verbose_name = _("Date et heure")


class StyleParagraph(Style):
    content = models.TextField(
        _("Contenu"),
        help_text=_("Texte à afficher"),
        max_length=1024,
    )

    class Meta:
        verbose_name = _("Texte libre")

    def _render_user_template(self, base_context):
        # User template have only access to pure json elements for security reasons
        inner_context = {
            # TODO rename to `submission_data` (& migrate sections) to match new naming
            "request_data": base_context["request_data"],
            "form_data": base_context["form_data"],
        }
        if "transaction_data" in base_context:
            inner_context["transaction_data"] = base_context["transaction_data"]

        env = SandboxedEnvironment()
        rendered_html = env.from_string(self.content).render(inner_context)
        result = (
            BeautifulSoup(mark_safe(rendered_html))
            .get_text()
            .replace("\r", " \A ")
            .replace("\n", " \A ")
        )
        return result

    def prepare_context(self, request, base_context):
        # Return updated context
        return {
            **super().prepare_context(request, base_context),
            "rendered_content": self._render_user_template(base_context),
        }


class StyleLogo(Style):
    logo = BackgroundFileField(
        _("Logo"),
        upload_to="backgound_paper",
        help_text=_("Image pour logo (PNG ou SVG)."),
        validators=[FileExtensionValidator(allowed_extensions=["svg", "png"])],
    )

    height = models.PositiveIntegerField(
        _("Hauteur"),
        default=60,
        help_text=_(
            "Défini la taille de l'image en %. Choisir un nombre compris entre 0 et 100"
        ),
    )

    class Meta:
        verbose_name = _("Logo")
