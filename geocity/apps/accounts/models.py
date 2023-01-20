from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.gis.db import models as geomodels
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.db.models import BooleanField, Count, ExpressionWrapper, Q, UniqueConstraint
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from taggit.managers import TaggableManager

from .fields import AdministrativeEntityFileField

# Controls who can fill each Form
PUBLIC_TYPE_CHOICES = (
    (
        True,
        _("Permettre la saisie à n'importe quel utilisateur disposant d'un compte"),
    ),
    (
        False,
        _(
            "Restreindre la saisie aux utilisateurs faisant partie de l'entité administrative"
        ),
    ),
)


class SiteProfile(models.Model):
    site = models.OneToOneField(
        Site,
        on_delete=models.CASCADE,
        related_name="site_profile",
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        default=None,
        on_delete=models.SET_NULL,
        verbose_name=_("Intégrateur"),
        related_name="site_profiles",
        limit_choices_to={"permit_department__is_integrator_admin": True},
    )
    custom_template = models.ForeignKey(
        "TemplateCustomization",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        verbose_name=_("Page de login"),
    )

    class Meta:
        verbose_name = _(
            "Paramètres complémentaires (à définir après avoir créé le site)"
        )
        verbose_name_plural = _(
            "Paramètres complémentaires (à définir après avoir créé le site)"
        )


@receiver(post_save, sender=Site)
def save_site_profile(sender, instance, created, **kwargs):
    if created or not SiteProfile.objects.filter(site=instance).exists():
        SiteProfile.objects.create(
            site=instance,
        )


class TemplateCustomization(models.Model):
    templatename = models.CharField(
        _("Identifiant"),
        max_length=64,
        blank=True,
        help_text="Permettant d'afficher la page de login par l'url: https://geocity.ch/?template=vevey",
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_]*$",
                message="Seuls les caractères sans accents et les chiffres sont autorisés. Les espaces et autres caractères spéciaux ne sont pas autorisés",
            )
        ],
    )
    application_title = models.CharField(_("Titre"), max_length=255, blank=True)
    application_subtitle = models.CharField(_("Sous-titre"), max_length=255, blank=True)
    application_description = models.TextField(
        _("Description"), max_length=2048, blank=True
    )
    background_image = models.ImageField(
        _("Image de fond"),
        blank=True,
        upload_to="background_images/",
        validators=[
            FileExtensionValidator(allowed_extensions=["svg", "png", "jpg", "jpeg"])
        ],
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=["templatename"], name="unique_template_name")
        ]
        verbose_name = _("4.1 Configuration de la page de login")
        verbose_name_plural = _("4.1 Configuration des pages de login")

    def __str__(self):
        return self.templatename


class PermitDepartment(models.Model):
    group = models.OneToOneField(
        Group, on_delete=models.CASCADE, related_name="permit_department"
    )
    description = models.CharField(_("description"), max_length=100, default="Service")
    shortname = models.CharField(
        _("nom court"),
        max_length=32,
        help_text=_(
            "Nom affiché par défaut dans les différentes étapes du formulaire, ne s'affiche pas dans l'admin (max. 32 caractères)"
        ),
        blank=True,
    )
    is_validator = models.BooleanField(
        _("validateur"),
        help_text=_(
            "Cocher si les membres doivent apparaître dans la liste des services consultables pour la validation"
        ),
    )
    is_backoffice = models.BooleanField(
        _("secrétariat"),
        default=False,
        help_text=_(
            "Cocher si les membres font partie du secrétariat. Ils seront notifiés des évolutions de la demande"
        ),
    )
    administrative_entity = models.ForeignKey(
        "AdministrativeEntity",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="departments",
        verbose_name=_("entité administrative"),
    )
    is_default_validator = models.BooleanField(
        _("sélectionné par défaut pour les validations"), default=False
    )
    integrator = models.IntegerField(
        _("Groupe des administrateurs"),
        help_text=_("Identifiant du groupe"),
        default=0,
    )
    is_integrator_admin = models.BooleanField(
        _("Intégrateur"),
        help_text=_("Cocher si les membres peuvent accéder à l'admin de Django"),
        default=False,
    )
    mandatory_2fa = models.BooleanField(
        _("2FA obligatoire"),
        help_text=_(
            "Cocher si les membres doivent obligatoirement utiliser la double authentification"
        ),
        default=False,
    )
    integrator_email_domains = models.CharField(
        _("Domaines d'emails visibles pour l'intégrateur"),
        help_text=_(
            "Liste de domaines séparés par des virgules ',' correspondant aux utilisateurs rattachés à l'entité administrative (ex: ma-commune.ch,commune.ch)"
        ),
        blank=True,
        max_length=254,
    )
    integrator_emails_exceptions = models.CharField(
        _("Emails complets visibles pour l'intégrateur"),
        help_text=_(
            "Liste d'emails séparés par des virgules ',' d'utilisateurs spécifiques rattachés à l'entité administrative (ex: greffe@nowhere.com)"
        ),
        blank=True,
        max_length=254,
    )

    class Meta:
        verbose_name = _("2.1 Configuration du service (pilote, validateur...)")
        verbose_name_plural = _(
            "2.1 Configuration des services (pilote, validateur...)"
        )

    def __str__(self):
        return str(self.group)


class AdministrativeEntityQuerySet(models.QuerySet):
    def filter_by_tags(self, tags):
        return self.filter(tags__name__in=[tag.lower() for tag in tags])


class AdministrativeEntityManager(models.Manager):
    def get_queryset(self):
        return AdministrativeEntityQuerySet(self.model)

    def public(self):
        return self.get_queryset().filter(anonymous_user__isnull=False)

    def associated_to_user(self, user):
        """
        Get the administrative entities associated to a specific user.
        If the users has entities, he's a trusted user
        """
        return (
            self.get_queryset()
            .filter(
                departments__group__in=user.groups.all(),
            )
            .order_by("ofs_id", "-name")
        )


class AdministrativeEntity(models.Model):
    name = models.CharField(_("name"), max_length=128)
    ofs_id = models.PositiveIntegerField(_("Numéro OFS"))
    link = models.URLField(_("Lien"), max_length=200, blank=True)
    archive_link = models.URLField(_("Archives externes"), max_length=1024, blank=True)
    general_informations = models.CharField(
        _("Informations"),
        blank=True,
        max_length=1024,
    )
    custom_signature = models.TextField(
        _("Signature des emails"),
        help_text=_("Si vide, le nom de l'entité sera utilisé"),
        max_length=1024,
        blank=True,
    )
    phone = models.CharField(
        _("Téléphone"),
        blank=True,
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^(((\+41)\s?)|(0))?(\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$",
                message="Seuls les chiffres et les espaces sont autorisés.",
            )
        ],
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
        limit_choices_to={"permit_department__is_integrator_admin": True},
    )
    additional_searchtext_for_address_field = models.CharField(
        _("Filtre additionnel pour la recherche d'adresse"),
        max_length=255,
        blank=True,
        help_text=_(
            'Ex: "Yverdon-les-Bains" afin de limiter les recherches à Yverdon, <a href="https://api3.geo.admin.ch/services/sdiservices.html#search" target="_blank">Plus d\'informations</a>'
        ),
    )
    geom = geomodels.MultiPolygonField(_("geom"), null=True, srid=2056)
    tags = TaggableManager(
        blank=True,
        verbose_name=_("Mots-clés"),
        help_text="Mots clefs sans espaces, séparés par des virgules permettant de filtrer les entités par l'url: https://geocity.ch/?entityfilter=yverdon",
    )
    expeditor_name = models.CharField(
        _("Nom de l'expéditeur des notifications"), max_length=255, blank=True
    )
    expeditor_email = models.CharField(
        _("Adresse email de l'expéditeur des notifications"),
        max_length=255,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,63}$",
                message="Le format de l'adresse email n'est pas valable.",
            )
        ],
    )
    is_single_form_submissions = models.BooleanField(
        _("Autoriser uniquement un objet par demande"),
        default=False,
        help_text=_("Nécessaire pour l'utilisation du système de paiement en ligne"),
    )

    sites = models.ManyToManyField(
        Site,
        related_name="+",
        verbose_name=_("Détails du Site"),
    )
    directive = AdministrativeEntityFileField(
        _("directive"),
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        blank=True,
    )
    directive_description = models.CharField(
        _("description de la directive"), max_length=200, blank=True
    )
    additional_information = models.TextField(_("autre information"), blank=True)

    objects = AdministrativeEntityManager()

    class Meta:
        verbose_name = _(
            "1.1 Configuration de l'entité administrative (commune, organisation)"
        )
        verbose_name_plural = _(
            "1.1 Configuration des entités administratives (commune, organisation)"
        )

    def __str__(self):
        return self.name

    def create_anonymous_user(self):
        try:
            return self.anonymous_user
        except ObjectDoesNotExist:
            username = "%s%s" % (settings.ANONYMOUS_USER_PREFIX, self.pk)
            first_name = "Anonymous user"
            last_name = self.name

            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                is_active=False,
            )

            return UserProfile.objects.create(
                administrative_entity=self,
                user_id=user.id,
                zipcode=settings.ANONYMOUS_USER_ZIPCODE,
            )

    def clean(self):
        from geocity.apps.forms.models import Form
        from geocity.apps.submissions.models import Submission

        if (
            Form.objects.annotate(entities_count=Count("administrative_entities"))
            .filter(
                is_public=True, entities_count__gt=1, administrative_entities=self.pk
            )
            .exists()
        ):
            raise ValidationError(
                _(
                    "Des formulaires partagés avec d'autres entités "
                    "administratives sont encore disponibles."
                )
            )

        if (
            self.is_single_form_submissions
            and Submission.objects.annotate(forms_count=Count("forms"))
            .filter(
                administrative_entity_id=self.pk,
                forms_count__gt=1,
            )
            .exclude(status=Submission.STATUS_ARCHIVED)
            .exists()
        ):
            raise ValidationError(
                {
                    "is_single_form_submissions": _(
                        "Impossible tant que des demandes liées à plusieurs "
                        "formulaires sont encore actives dans cette entité "
                        "administrative."
                    )
                }
            )

        if (
            not self.is_single_form_submissions
            and Form.objects.filter(
                requires_online_payment=True, administrative_entities=self
            ).exists()
        ):
            raise ValidationError(
                {
                    "is_single_form_submissions": _(
                        "Il existe encore des formulaires soumis au paiement en ligne "
                        "dans cette entité administrative. Avant de permettre les "
                        "demandes à objets multiples, veuillez supprimer ces "
                        "formulaires ou y désactiver le paiement en ligne."
                    )
                }
            )


# Change the app_label in order to regroup models under the same app in admin
class AdministrativeEntityForAdminSite(AdministrativeEntity):
    class Meta:
        proxy = True
        app_label = "forms"
        verbose_name = _("1.1 Entité administrative")
        verbose_name_plural = _("1.1 Entités administratives")


class UserProfileManager(models.Manager):
    def create_temporary_user(self, entity):
        # TODO should this be moved to User instead of UserProfile?
        # TODO why isn’t the `entity` argument used?
        # Multiple temp users might exist at the same time
        last_temp_user = self.get_queryset().filter(is_temporary=True).last()
        if last_temp_user:
            nb = int(last_temp_user.user.username.split("_")[2]) + 1
        else:
            nb = 0

        username = "%s%s" % (settings.TEMPORARY_USER_PREFIX, nb)
        email = "%s@%s" % (username, settings.SITE_DOMAIN)
        zipcode = settings.TEMPORARY_USER_ZIPCODE

        temp_user = User.objects.create_user(
            username, email, password=None, first_name="Temporaire", last_name="Anonyme"
        )

        new_temp_author = super().create(
            user=temp_user,
            zipcode=zipcode,
        )

        return new_temp_author

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                is_temporary=ExpressionWrapper(
                    Q(user__username__startswith=settings.TEMPORARY_USER_PREFIX),
                    output_field=BooleanField(),
                )
            )
        )


class UserProfile(models.Model):
    company_name = models.CharField(_("Raison Sociale"), max_length=100, blank=True)
    vat_number = models.CharField(
        _("Numéro TVA"),
        max_length=19,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^(CHE-)+\d{3}\.\d{3}\.\d{3}(\sTVA)?$",
                message="Le code d'entreprise doit être de type \
                         CHE-123.456.789 (TVA) \
                         et vous pouvez le trouver sur \
                         le registre fédéral des entreprises \
                         https://www.uid.admin.ch/search.aspx",
            )
        ],
    )
    address = models.CharField(
        _("Rue"),
        max_length=100,
    )
    zipcode = models.PositiveIntegerField(
        _("NPA"),
        validators=[MinValueValidator(1000), MaxValueValidator(9999)],
    )
    city = models.CharField(
        _("Ville"),
        max_length=100,
    )
    phone_first = models.CharField(
        _("Téléphone principal"),
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^(((\+41)\s?)|(0))?(\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$",
                message="Seuls les chiffres et les espaces sont autorisés.",
            )
        ],
    )
    phone_second = models.CharField(
        _("Téléphone secondaire"),
        blank=True,
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^(((\+41)\s?)|(0))?(\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$",
                message="Seuls les chiffres et les espaces sont autorisés.",
            )
        ],
    )
    iban = models.CharField(
        _("IBAN"),
        help_text=_(
            "A remplir uniquement pour les prestations liées à un remboursement (le titulaire du compte doit correspondre aux informations indiquées ci-dessus)."
        ),
        blank=True,
        max_length=30,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{2}[0-9]{2}(?:[ ]?[0-9A-Z]{4}){4}(?:[ ]?[0-9]{1,2})?$",
                message="L'IBAN doit être de type CH12 3456 7890 1234 5678 9",
            )
        ],
    )
    notify_per_email = models.BooleanField(_("Me notifier par e-mail"), default=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    history = HistoricalRecords()

    administrative_entity = models.OneToOneField(
        AdministrativeEntity,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="anonymous_user",
        verbose_name=_("entité administrative"),
    )

    objects = UserProfileManager()

    def clean(self):
        if self.user and self.user.is_active and self.administrative_entity is not None:
            raise ValidationError(
                _(
                    "Seul·e un·e auteur désactivé·e peut être relié directement "
                    "à une entité administrative, et ainsi être considéré·e "
                    "auteur·e anonyme de l'entité."
                )
            )

    @cached_property
    def is_anonymous(self):
        """
        UserProfile unique per AdministrativeEntity.
        Never logged in. Used to save anonymous requests.
        """
        return (
            self.user
            and not self.user.is_active
            and self.administrative_entity is not None
        )

    @cached_property
    def is_temporary(self):
        """
        UserProfile created when starting an anonymous submission,
        then deleted at the submission (replaced by an anonymous user).
        """
        return self.user and self.user.username.startswith(
            settings.TEMPORARY_USER_PREFIX
        )

    class Meta:
        verbose_name = _("3.2 Consultation de l'auteur")
        verbose_name_plural = _("3.2 Consultation des auteurs")

    def get_absolute_url(self):
        # FIXME this URL name doesn’t exist, but that was already the case before the
        # phoenix migration. Should we remove this?
        return reverse("accounts:genericauthorview", args=[str(self.id)])

    def __str__(self):

        return (
            str(self.user.first_name) + " " + str(self.user.last_name)
            if self.user
            else str(self.pk)
        )
