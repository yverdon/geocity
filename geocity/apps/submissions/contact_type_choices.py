from django.utils.translation import gettext_lazy as _

# Contact types
CONTACT_TYPE_OTHER = 0
CONTACT_TYPE_REQUESTOR = 1
CONTACT_TYPE_OWNER = 2
CONTACT_TYPE_COMPANY = 3
CONTACT_TYPE_CLIENT = 4
CONTACT_TYPE_SECURITY = 5
CONTACT_TYPE_ASSOCIATION = 6
CONTACT_TYPE_ENGINEER = 7
CONTACT_TYPE_WORKDIRECTOR = 8
CONTACT_TYPE_CHOICES = (
    (CONTACT_TYPE_ENGINEER, _("Architecte/Ingénieur")),
    (CONTACT_TYPE_ASSOCIATION, _("Association")),
    (CONTACT_TYPE_OTHER, _("Autres")),
    (CONTACT_TYPE_WORKDIRECTOR, _("Direction des travaux")),
    (CONTACT_TYPE_COMPANY, _("Entreprise")),
    (CONTACT_TYPE_CLIENT, _("Maître d'ouvrage")),
    (CONTACT_TYPE_OWNER, _("Propriétaire")),
    (CONTACT_TYPE_REQUESTOR, _("Requérant (si différent de l'auteur de la demande)")),
    (CONTACT_TYPE_SECURITY, _("Sécurité")),
)
