import re
import unicodedata
from io import StringIO

from constance import config
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core import management
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.utils import timezone

from geomapshark import permissions_groups, settings
from permits import models
from reports.models import Report


def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicode(text, "utf-8")
    except (TypeError, NameError):  # unicode is a default on python 3
        pass
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore")
    text = text.decode("utf-8")
    return str(text)


def unaccent(text):
    """
    Convert input text to id.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    text = strip_accents(text.lower())
    text = re.sub("[ ]+", "_", text)
    text = re.sub("[^0-9a-zA-Z_-]", "", text)
    return text


User = get_user_model()


def reset_db():
    """
    Reset database to a blank state by removing all the tables and recreating them.
    """
    with transaction.atomic():
        with connection.cursor() as cursor:

            if settings.CLEAR_PUBLIC_SCHEMA_ON_FIXTURIZE.lower() == "true":
                cursor.execute(
                    "select tablename from pg_tables where schemaname = 'geocity' or schemaname = 'public'"
                )
                tables = [
                    row[0]
                    for row in cursor.fetchall()
                    if row[0] not in {"spatial_ref_sys"}
                ]
            else:  # some user might don't want to clear public schema
                cursor.execute(
                    "select tablename from pg_tables where schemaname = 'geocity'"
                )
                tables = [row[0] for row in cursor.fetchall()]
            # Can't use query parameters here as they'll add single quotes which are not
            # supported by postgres
            for table in tables:
                cursor.execute('drop table "' + table + '" cascade')

    # Call migrate so that post-migrate hooks such as generating a default Site object
    # are run.

    # sprint-7/yc-357: This was removed from the atomic transaction because
    # Addfield and AlterField operations are performed, thus generating a:
    # django.db.utils.OperationalError: cannot ALTER TABLE "permits_permitdepartment"
    # because it has pending trigger events.
    management.call_command("migrate", "--noinput", stdout=StringIO())


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Resetting database...")
        reset_db()
        with transaction.atomic():
            self.stdout.write("Setup Site objects...")
            self.setup_site()
            self.stdout.write("Creating users...")
            self.create_users()
            self.stdout.write("Creating works types and objs...")
            self.create_works_types()
            self.stdout.write("Creating demo permit...")
            self.create_permit()
            self.stdout.write("Creating dummy geometric entities...")
            self.create_geom_layer_entity()
            self.stdout.write("Creating template customizations...")
            self.setup_homepage()
            self.stdout.write("Setting integrator for selected confgurations...")
            self.setup_integrator()
            self.stdout.write("Fixturize succeed!")

    def setup_site(self):
        # default site, will not appear in admin
        site = Site.objects.get()
        site.name = "localhost"
        site.domain = "localhost"
        site.save()
        # custom sites
        models.Site.objects.create(
            domain="yverdon.localhost",
            name="yverdon",
            application_title="Geocity",
            application_subtitle="Demandes en lignes concenrnant le territoire communal",
            application_description="Demandes en ligne concernant le <b>domaine public</b>",
            background_color="#FFFFFF",
            login_background_color="#FFFFFF",
            primary_color="#008c6f",
            secondary_color="#01755d",
            text_color="#000000",
            title_color="#000000",
            table_color="#212529",
        )
        models.Site.objects.create(
            domain="grandson.localhost",
            name="grandson",
            application_title="Geocity",
            application_subtitle="Demandes en lignes concenrnant le territoire communal",
            application_description="Demandes en ligne concernant le <b>domaine public</b>",
            background_color="#FFFFFF",
            login_background_color="#FFFFFF",
            primary_color="#008c6f",
            secondary_color="#01755d",
            text_color="#000000",
            title_color="#000000",
            table_color="#212529",
        )
        models.Site.objects.create(
            domain="vevey.localhost",
            name="vevey",
            application_title="Geocity",
            application_subtitle="Demandes en lignes concenrnant le territoire communal",
            application_description="Demandes en ligne concernant le <b>domaine public</b>",
            background_color="#FFFFFF",
            login_background_color="#FFFFFF",
            primary_color="#008c6f",
            secondary_color="#01755d",
            text_color="#000000",
            title_color="#000000",
            table_color="#212529",
        )
        models.Site.objects.create(
            domain="lausanne.localhost",
            name="lausanne",
            application_title="Geocity",
            application_subtitle="Demandes en lignes concenrnant le territoire communal",
            application_description="Demandes en ligne concernant le <b>domaine public</b>",
            background_color="#FFFFFF",
            login_background_color="#FFFFFF",
            primary_color="#008c6f",
            secondary_color="#01755d",
            text_color="#000000",
            title_color="#000000",
            table_color="#212529",
        )

        # A domain with which all integrators cas associate their own created administrative entities
        models.Site.objects.create(
            domain=settings.BASE_DOMAIN,
            name="base common domain",
            application_title="City Admin",
            application_subtitle="Demandes en lignes",
            application_description="Demandes concernant l' <i>administration</i>",
            background_color="#FFFFFF",
            login_background_color="#FFFFFF",
            primary_color="#008c6f",
            secondary_color="#01755d",
            text_color="#000000",
            title_color="#000000",
            table_color="#212529",
        )

        # Site for internal use
        # TODO: we shouldn't need this ! Either we need forward the site for internal calls
        # or there should be a default site. For now this should have no impact because
        # the API is not filtered by site.
        # see https://github.com/yverdon/geocity/issues/525
        Site.objects.create(domain="web", name="web (internal calls)")

    def setup_integrator(self):
        integrator = Group.objects.get(name="integrator")
        models.Site.objects.filter(name="yverdon").update(integrator=integrator)
        models.PermitAdministrativeEntity.objects.update(integrator=integrator)
        models.WorksType.objects.update(integrator=integrator)
        models.WorksObject.objects.update(integrator=integrator)
        models.WorksObjectType.objects.update(integrator=integrator)
        models.PermitActorType.objects.update(integrator=integrator)
        models.ComplementaryDocumentType.objects.update(integrator=integrator)
        models.PermitRequestAmendProperty.objects.update(integrator=integrator)

    def create_users(self):

        administrative_entity_yverdon = models.PermitAdministrativeEntity.objects.create(
            name="Démo Yverdon",
            ofs_id=5938,
            link="https://mapnv.ch",
            archive_link="https://mapnv.ch",
            geom="SRID=2056;MultiPolygon (((2538391 1176432, 2538027 1178201, 2538485 1178804, 2537777 1179199, 2536748 1178450, 2536123 1179647, 2537382 1180593, 2537143 1181623, 2538651 1183257, 2540368 1183236, 2541252 1181093, 2541460 1180458, 2540160 1179543, 2540097 1178877, 2538391 1176432)))",
        )

        administrative_entity_yverdon.tags.add("yverdon")
        administrative_entity_yverdon.sites.add(Site.objects.get(name="yverdon"))
        administrative_entity_yverdon.sites.add(Site.objects.get(name="localhost"))

        administrative_entity_grandson = models.PermitAdministrativeEntity.objects.create(
            name="Démo Grandson",
            ofs_id=5938,
            link="https://mapnv.ch",
            archive_link="https://mapnv.ch",
            geom="SRID=2056;MultiPolygon (((2543281 1184952, 2542053 1186731, 2541148 1186887, 2538214 1186367, 2537195 1184609, 2537153 1183330, 2537757 1182653, 2539317 1182404, 2543281 1184952)))",
        )

        administrative_entity_grandson.tags.add("grandson")
        administrative_entity_grandson.sites.add(Site.objects.get(name="grandson"))
        administrative_entity_grandson.sites.add(Site.objects.get(name="localhost"))

        administrative_entity_lausanne = models.PermitAdministrativeEntity.objects.create(
            name="Démo Lausanne",
            ofs_id=5586,
            link="https://mapnv.ch",
            archive_link="https://mapnv.ch",
            geom="SRID=2056;MultiPolygon (((2533045 1151566, 2533789 1154840, 2538236 1155380, 2541064 1154989, 2541790 1157408, 2540934 1160087, 2543074 1161259, 2546553 1159715, 2545399 1156329, 2542757 1155361, 2542348 1153798, 2542497 1152347, 2540692 1150617, 2535855 1152105, 2533045 1151566)),((2529938 1157110, 2529789 1160329, 2532245 1161557, 2532580 1160273, 2530831 1158934, 2530757 1157259, 2529938 1157110)))",
        )

        administrative_entity_lausanne.tags.add("lausanne")
        administrative_entity_lausanne.sites.add(Site.objects.get(name="lausanne"))
        administrative_entity_lausanne.sites.add(Site.objects.get(name="localhost"))

        administrative_entity_vevey = models.PermitAdministrativeEntity.objects.create(
            name="Démo Vevey",
            ofs_id=5890,
            link="https://mapnv.ch",
            archive_link="https://mapnv.ch",
            geom="SRID=2056;MultiPolygon (((2553381 1146430, 2553679 1145798, 2553660 1145500, 2554777 1145296, 2555502 1145965, 2554870 1146617, 2555335 1147398, 2555037 1147417, 2554311 1146803, 2553418 1146840, 2553269 1146524, 2553381 1146430)))",
        )

        administrative_entity_vevey.tags.add("vevey")
        administrative_entity_vevey.sites.add(Site.objects.get(name="vevey"))
        administrative_entity_vevey.sites.add(Site.objects.get(name="localhost"))

        user = User.objects.create_user(
            email=f"yverdon-squad+admin@liip.ch",
            first_name="SuperAdmin",
            last_name="Demo",
            username="admin",
            password="demo",
            is_staff=True,
            is_superuser=True,
        )
        self.stdout.write("admin / demo")

        models.PermitAuthor.objects.create(
            user=user,
            address="Rue du test",
            zipcode=1234,
            city="Yverdon",
            phone_first="000 00 00 00",
            phone_second="000 00 00 00",
        )

        user = User.objects.create_user(
            username="user",
            password="demo",
            email=f"yverdon-squad+user@liip.ch",
            first_name="User",
            last_name="Demo",
        )
        models.PermitAuthor.objects.create(
            user=user,
            address="Rue du Port",
            zipcode=1234,
            city="Lausanne",
            phone_first="000 00 00 00",
            phone_second="000 00 00 00",
        )
        self.stdout.write("user / demo")

        permit_request_ct = ContentType.objects.get_for_model(models.PermitRequest)
        secretariat_permissions = Permission.objects.filter(
            codename__in=[
                "amend_permit_request",
                "classify_permit_request",
            ],
            content_type=permit_request_ct,
        )

        reports_request_ct = ContentType.objects.get_for_model(Report)
        secretariat_permissions_reports = Permission.objects.filter(
            codename__in=[
                "can_generate_pdf",
            ],
            content_type=reports_request_ct,
        )
        user = self.create_user(
            "pilot",
            "pilot",
            administrative_entity_yverdon,
            email="yverdon-squad+pilot@liip.ch",
        )
        user.user_permissions.set(
            secretariat_permissions.union(secretariat_permissions_reports)
        )
        self.stdout.write("pilot / demo")

        user = self.create_user(
            "pilot-2",
            "pilot-2",
            administrative_entity_grandson,
            email="yverdon-squad+pilot-2@liip.ch",
        )
        user.user_permissions.set(secretariat_permissions)
        self.stdout.write("pilot-2 / demo")

        secretary_groups = Group.objects.filter(name__in=["pilot", "pilot-2"])
        department = models.PermitDepartment.objects.filter(
            group__in=secretary_groups
        ).update(is_backoffice=True)

        user = self.create_user(
            "validator",
            "validator",
            administrative_entity_yverdon,
            is_default_validator=True,
            email="yverdon-squad+validator@liip.ch",
        )
        Group.objects.get(name="validator").permissions.add(
            Permission.objects.get(
                codename="validate_permit_request", content_type=permit_request_ct
            )
        )

        validator_group = Group.objects.get(name="validator")
        departement = models.PermitDepartment.objects.get(group=validator_group)
        departement.is_validator = True
        departement.save()

        self.stdout.write("validator / demo")

        user = self.create_user(
            "validator-2",
            "validator-2",
            administrative_entity_yverdon,
            email="yverdon-squad+validator-2@liip.ch",
        )
        Group.objects.get(name="validator-2").permissions.add(
            Permission.objects.get(
                codename="validate_permit_request", content_type=permit_request_ct
            )
        )
        self.stdout.write("validator-2 / demo")

        user = self.create_user(
            "integrator",
            "integrator",
            administrative_entity_yverdon,
            is_default_validator=True,
            is_integrator_admin=True,
            is_staff=True,
            email="yverdon-squad+integrator@liip.ch",
        )

        permits_permissions = Permission.objects.filter(
            content_type__app_label="permits",
            content_type__model__in=permissions_groups.INTEGRATOR_PERMITS_MODELS_PERMISSIONS,
        )
        report_permissions = Permission.objects.filter(
            content_type__app_label="reports",
            content_type__model__in=permissions_groups.INTEGRATOR_REPORTS_MODELS_PERMISSIONS,
        )

        other_permissions = Permission.objects.filter(
            codename__in=permissions_groups.OTHER_PERMISSIONS_CODENAMES
        )
        # set the required permissions for the integrator group
        Group.objects.get(name="integrator").permissions.set(
            permits_permissions.union(other_permissions).union(report_permissions)
        )
        self.stdout.write("integrator / demo")

        # Insert status choices from PermitRequest and insert status for adminsitrative_entity
        for status_value in models.PermitRequest.STATUS_CHOICES:
            for entity in [
                administrative_entity_yverdon,
                administrative_entity_grandson,
                administrative_entity_lausanne,
                administrative_entity_vevey,
            ]:
                models.PermitWorkflowStatus.objects.get_or_create(
                    status=status_value[0], administrative_entity=entity
                )
        # Add admin user in all groups
        groups = Group.objects.all()
        user_admin = User.objects.get(username="admin")
        for group in groups:
            user_admin.groups.add(group)

    def create_user(
        self,
        username,
        group_name,
        administrative_entity,
        is_default_validator=False,
        is_integrator_admin=False,
        is_staff=False,
        email="yverdon-squad+user@liip.ch",
    ):

        group, created = Group.objects.get_or_create(name=group_name)
        user = User.objects.create_user(
            email=email,
            first_name="User First",
            last_name="User Last",
            username=username,
            password="demo",
            is_staff=is_staff,
        )
        user.groups.set([group])
        models.PermitAuthor.objects.create(
            user=user,
            address="Rue du Lac",
            zipcode=1400,
            city="Yverdon",
        )
        models.PermitDepartment.objects.create(
            group=group,
            is_validator=False,
            is_integrator_admin=is_integrator_admin,
            is_backoffice=False,
            administrative_entity=administrative_entity,
            is_default_validator=is_default_validator,
        )

        return user

    def create_works_types(self):
        properties = {
            "title": models.WorksObjectProperty.objects.create(
                name="Texte permettant de séparer visuellement les champs",
                input_type="title",
                help_text="Ce texte permet d'expliquer en détail à l'utilisateur les pourquoi et le comment des informations à fournir",
                is_mandatory=False,
                order=2,
            ),
            "comment": models.WorksObjectProperty.objects.create(
                name="Commentaire", input_type="text", is_mandatory=False, order=0
            ),
            "width": models.WorksObjectProperty.objects.create(
                name="Largeur [m]",
                input_type="number",
                placeholder="3",
                help_text="Largeur en mètres",
                is_mandatory=False,
                order=1,
            ),
            "height": models.WorksObjectProperty.objects.create(
                name="Hauteur [m]",
                input_type="number",
                placeholder="2",
                help_text="Longueur en mètres",
                is_mandatory=False,
                order=3,
            ),
            "plan": models.WorksObjectProperty.objects.create(
                name="Plan de situation",
                input_type="file",
                help_text="Plan complémentaire détaillant votre projet",
                is_mandatory=False,
                order=4,
            ),
            "adresse": models.WorksObjectProperty.objects.create(
                name="Adresse",
                input_type="address",
                placeholder="Place Pestalozzi 2, 1400 Yverdon-les-Bains",
                is_mandatory=False,
                order=5,
            ),
            "adresse_geocode": models.WorksObjectProperty.objects.create(
                name="Adresse avec géocodage",
                input_type="address",
                placeholder="Place Pestalozzi 2, 1400 Yverdon-les-Bains",
                is_mandatory=False,
                store_geometry_for_address_field=True,
                order=5,
            ),
            "date": models.WorksObjectProperty.objects.create(
                name="Date",
                input_type="date",
                is_mandatory=False,
                order=6,
            ),
            "checkbox": models.WorksObjectProperty.objects.create(
                name="Impact sur la chaussée",
                input_type="checkbox",
                is_mandatory=False,
                order=7,
            ),
            "list_single": models.WorksObjectProperty.objects.create(
                name="À moins de 3m d'un arbre",
                input_type="list_single",
                is_mandatory=False,
                choices="oui\nnon",
                order=8,
            ),
            "list_multiple": models.WorksObjectProperty.objects.create(
                name="À moins de 3m d'un arbre",
                input_type="list_multiple",
                is_mandatory=False,
                choices="Déviation trafic\nHoraire prolongé\nSon>90dB",
                order=9,
            ),
        }
        works_types = [
            (
                "Stationnement (ex. de demande devant être prolongée)",
                [
                    (
                        "Demande de macaron",
                        properties["comment"],
                        properties["date"],
                    ),
                    (
                        "Accès au centre-ville historique",
                        properties["plan"],
                        properties["width"],
                        properties["comment"],
                        properties["title"],
                        properties["date"],
                        properties["checkbox"],
                        properties["adresse"],
                        properties["list_multiple"],
                    ),
                ],
            ),
            (
                "Événements sur la voie publique",
                [
                    (
                        "Événement sportif",
                        properties["plan"],
                        properties["width"],
                        properties["comment"],
                        properties["title"],
                        properties["date"],
                        properties["checkbox"],
                        properties["adresse"],
                        properties["list_multiple"],
                    ),
                    (
                        "Événement culturel",
                        properties["plan"],
                        properties["width"],
                        properties["comment"],
                        properties["title"],
                        properties["date"],
                        properties["checkbox"],
                        properties["adresse"],
                        properties["list_multiple"],
                    ),
                    (
                        "Événement politique",
                        properties["plan"],
                        properties["width"],
                        properties["comment"],
                        properties["title"],
                        properties["date"],
                        properties["checkbox"],
                        properties["adresse"],
                        properties["list_multiple"],
                    ),
                    (
                        "Événement commercial",
                        properties["plan"],
                        properties["width"],
                        properties["comment"],
                        properties["title"],
                        properties["date"],
                        properties["checkbox"],
                        properties["adresse"],
                        properties["list_multiple"],
                    ),
                ],
            ),
            (
                "Chantier",
                [
                    (
                        "Permis de fouille",
                        properties["width"],
                        properties["height"],
                        properties["title"],
                        properties["comment"],
                        properties["adresse"],
                        properties["adresse_geocode"],
                        properties["checkbox"],
                        properties["list_single"],
                    ),
                    (
                        "Permis de dépôt",
                        properties["width"],
                        properties["height"],
                        properties["comment"],
                        properties["title"],
                        properties["adresse"],
                        properties["adresse_geocode"],
                        properties["checkbox"],
                    ),
                ],
            ),
            (
                "Suvbentions (ex. de demande sans géométrie ni période temporelle)",
                [
                    (
                        "Prime éco-mobilité",
                        properties["comment"],
                    ),
                    (
                        "Abonnement de bus",
                        properties["comment"],
                    ),
                ],
            ),
        ]
        administrative_entity_yverdon = models.PermitAdministrativeEntity.objects.get(
            name="Démo Yverdon",
        )
        administrative_entity_yverdon.tags.add("yverdon")
        administrative_entity_grandson = models.PermitAdministrativeEntity.objects.get(
            name="Démo Grandson",
        )
        administrative_entity_grandson.tags.add("grandson")
        administrative_entity_lausanne = models.PermitAdministrativeEntity.objects.get(
            name="Démo Lausanne",
        )
        administrative_entity_lausanne.tags.add("lausanne")
        administrative_entity_vevey = models.PermitAdministrativeEntity.objects.get(
            name="Démo Vevey",
        )
        administrative_entity_vevey.tags.add("vevey")

        additional_information_text = """
        Texte expliquant la ou les conditions particulière(s) s'appliquant à cette demande.
        Un document pdf peut également être proposé à l'utilisateur, par exemple pour les conditions
        de remise en état après une fouille sur le domaine public
        """

        for works_type, objs in works_types:
            works_type_obj = models.WorksType.objects.create(name=works_type)
            works_type_obj.tags.add(unaccent(works_type))
            models.PermitActorType.objects.create(
                type=models.ACTOR_TYPE_OTHER,
                works_type=works_type_obj,
                is_mandatory=False,
            )

            for works_obj, *props in objs:
                works_obj_obj, created = models.WorksObject.objects.get_or_create(
                    name=works_obj
                )
                works_object_type = models.WorksObjectType.objects.create(
                    works_type=works_type_obj,
                    works_object=works_obj_obj,
                    is_public=True,
                    notify_services=True,
                    document_enabled=True,
                    publication_enabled=True,
                    permanent_publication_enabled=True,
                    services_to_notify=f"yverdon-squad+admin@liip.ch",
                    additional_information=additional_information_text,
                )
                works_object_type.administrative_entities.add(
                    administrative_entity_yverdon
                )
                works_object_type.administrative_entities.add(
                    administrative_entity_grandson
                )
                works_object_type.administrative_entities.add(
                    administrative_entity_lausanne
                )
                works_object_type.administrative_entities.add(
                    administrative_entity_vevey
                )
                self.create_document_types(works_object_type)
                for prop in props:
                    prop.works_object_types.add(works_object_type)

        # Configure specific WOT in order to illustrate full potential of Geocity

        # No geom nor time
        for wot in models.WorksObjectType.objects.filter(
            works_type__name="Suvbentions (ex. de demande sans géométrie ni période temporelle)"
        ):
            wot.has_geometry_point = False
            wot.has_geometry_line = False
            wot.has_geometry_polygon = False
            wot.needs_date = False
            wot.save()

        # Renewal reminder
        for wot in models.WorksObjectType.objects.filter(
            works_type__name="Stationnement (ex. de demande devant être prolongée)"
        ):
            wot.has_geometry_point = True
            wot.has_geometry_line = False
            wot.has_geometry_polygon = False
            wot.needs_date = True
            wot.start_delay = 1
            wot.permit_duration = 2
            wot.expiration_reminder = True
            wot.days_before_reminder = 5
            wot.save()

    def create_permit(self):

        demo_user = User.objects.get(username="user")
        demo_author = models.PermitAuthor.objects.get(id=demo_user.id)
        demo_administrative_entity = models.PermitAdministrativeEntity.objects.get(
            name="Démo Yverdon"
        )
        demo_works_object_type = models.WorksObjectType.objects.first()
        models.WorksObjectType.objects.filter(id=5).update(
            requires_validation_document=False
        )
        demo_works_object_type_no_validation_document = (
            models.WorksObjectType.objects.filter(
                requires_validation_document=False
            ).first()
        )
        department = models.PermitDepartment.objects.filter(
            administrative_entity=demo_administrative_entity,
            is_validator=True,
        ).first()

        # Basic permit request
        permit_request = models.PermitRequest.objects.create(
            status=models.PermitRequest.STATUS_DRAFT,
            administrative_entity=demo_administrative_entity,
            author=demo_author,
        )

        models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request, works_object_type=demo_works_object_type
        )

        models.PermitRequestGeoTime.objects.create(
            permit_request=permit_request,
            starts_at=timezone.now(),
            ends_at=timezone.now(),
            geom="GEOMETRYCOLLECTION(MULTILINESTRING((2539096.09997796 1181119.41274907,2539094.37477054 1181134.07701214,2539094.37477054 1181134.07701214)), MULTIPOLYGON(((2539102.56950579 1181128.03878617,2539101.27560022 1181139.2526344,2539111.19554289 1181140.11523811,2539111.62684475 1181134.07701214,2539111.62684475 1181134.07701214,2539102.56950579 1181128.03878617))), MULTIPOINT((2539076.69139448 1181128.47008802)))",
        )

        # Permit Request to Classify with no validation document required
        permit_request2 = models.PermitRequest.objects.create(
            status=models.PermitRequest.STATUS_PROCESSING,
            administrative_entity=demo_administrative_entity,
            author=demo_author,
            is_public=True,
        )

        models.PermitRequestValidation.objects.get_or_create(
            permit_request=permit_request2,
            department=department,
            validation_status=models.PermitRequestValidation.STATUS_APPROVED,
            comment_before="Ce projet n'est pas admissible, veuillez l'améliorer.",
            comment_during="Les améliorations ont été prise en compte.",
            comment_after="Excellent projet qui bénéficiera à la communauté.",
        )

        models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request2,
            works_object_type=demo_works_object_type_no_validation_document,
        )

        models.PermitRequestGeoTime.objects.create(
            permit_request=permit_request2,
            starts_at=timezone.now(),
            ends_at=timezone.now(),
            geom="GEOMETRYCOLLECTION(MULTILINESTRING((2539096.09997796 1181119.41274907,2539094.37477054 1181134.07701214,2539094.37477054 1181134.07701214)), MULTIPOLYGON(((2539102.56950579 1181128.03878617,2539101.27560022 1181139.2526344,2539111.19554289 1181140.11523811,2539111.62684475 1181134.07701214,2539111.62684475 1181134.07701214,2539102.56950579 1181128.03878617))), MULTIPOINT((2539076.69139448 1181128.47008802)))",
        )

        # Permit Request to Classify with mixed objects requiring and not requiring validation document
        permit_request3 = models.PermitRequest.objects.create(
            status=models.PermitRequest.STATUS_PROCESSING,
            administrative_entity=demo_administrative_entity,
            author=demo_author,
            is_public=True,
        )

        models.PermitRequestValidation.objects.get_or_create(
            permit_request=permit_request3,
            department=department,
            validation_status=models.PermitRequestValidation.STATUS_APPROVED,
            comment_before="Ce projet n'est pas admissible, veuillez l'améliorer.",
            comment_during="Les améliorations ont été prise en compte.",
            comment_after="Excellent projet qui bénéficiera à la communauté.",
        )

        models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request3, works_object_type=demo_works_object_type
        )

        models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request3,
            works_object_type=demo_works_object_type_no_validation_document,
        )

        models.PermitRequestGeoTime.objects.create(
            permit_request=permit_request3,
            starts_at=timezone.now(),
            ends_at=timezone.now(),
            geom="GEOMETRYCOLLECTION(MULTILINESTRING((2539096.09997796 1181119.41274907,2539094.37477054 1181134.07701214,2539094.37477054 1181134.07701214)), MULTIPOLYGON(((2539102.56950579 1181128.03878617,2539101.27560022 1181139.2526344,2539111.19554289 1181140.11523811,2539111.62684475 1181134.07701214,2539111.62684475 1181134.07701214,2539102.56950579 1181128.03878617))), MULTIPOINT((2539076.69139448 1181128.47008802)))",
        )

        # Permit Requests to Classify with validation document required
        permit_request4 = models.PermitRequest.objects.create(
            status=models.PermitRequest.STATUS_PROCESSING,
            administrative_entity=demo_administrative_entity,
            author=demo_author,
            is_public=True,
        )

        models.PermitRequestValidation.objects.get_or_create(
            permit_request=permit_request4,
            department=department,
            validation_status=models.PermitRequestValidation.STATUS_APPROVED,
            comment_before="Ce projet n'est pas admissible, veuillez l'améliorer.",
            comment_during="Les améliorations ont été prise en compte.",
            comment_after="Excellent projet qui bénéficiera à la communauté.",
        )
        models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request4, works_object_type=demo_works_object_type
        )

        models.PermitRequestGeoTime.objects.create(
            permit_request=permit_request4,
            starts_at=timezone.now(),
            ends_at=timezone.now(),
            geom="GEOMETRYCOLLECTION(MULTILINESTRING((2539096.09997796 1181119.41274907,2539094.37477054 1181134.07701214,2539094.37477054 1181134.07701214)), MULTIPOLYGON(((2539102.56950579 1181128.03878617,2539101.27560022 1181139.2526344,2539111.19554289 1181140.11523811,2539111.62684475 1181134.07701214,2539111.62684475 1181134.07701214,2539102.56950579 1181128.03878617))), MULTIPOINT((2539076.69139448 1181128.47008802)))",
        )

        permit_request5 = models.PermitRequest.objects.create(
            status=models.PermitRequest.STATUS_PROCESSING,
            administrative_entity=demo_administrative_entity,
            author=demo_author,
            is_public=True,
        )

        models.PermitRequestValidation.objects.get_or_create(
            permit_request=permit_request5,
            department=department,
            validation_status=models.PermitRequestValidation.STATUS_APPROVED,
            comment_before="Ce projet n'est pas admissible, veuillez l'améliorer.",
            comment_during="Les améliorations ont été prise en compte.",
            comment_after="Excellent projet qui bénéficiera à la communauté.",
        )

        models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request5,
            works_object_type=models.WorksObjectType.objects.last(),
        )

        models.PermitRequestGeoTime.objects.create(
            permit_request=permit_request5,
            starts_at=timezone.now(),
            ends_at=timezone.now(),
            geom="GEOMETRYCOLLECTION(MULTILINESTRING((2539096.09997796 1181119.41274907,2539094.37477054 1181134.07701214,2539094.37477054 1181134.07701214)), MULTIPOLYGON(((2539102.56950579 1181128.03878617,2539101.27560022 1181139.2526344,2539111.19554289 1181140.11523811,2539111.62684475 1181134.07701214,2539111.62684475 1181134.07701214,2539102.56950579 1181128.03878617))), MULTIPOINT((2539076.69139448 1181128.47008802)))",
        )

        # permit with pending validations

        permit_request6 = models.PermitRequest.objects.create(
            status=models.PermitRequest.STATUS_AWAITING_VALIDATION,
            administrative_entity=demo_administrative_entity,
            author=demo_author,
            is_public=True,
        )

        models.PermitRequestValidation.objects.get_or_create(
            permit_request=permit_request6,
            department=department,
        )

        models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request6,
            works_object_type=models.WorksObjectType.objects.last(),
        )

        models.PermitRequestGeoTime.objects.create(
            permit_request=permit_request6,
            starts_at=timezone.now(),
            ends_at=timezone.now(),
            geom="GEOMETRYCOLLECTION(MULTILINESTRING((2539096.09997796 1181119.41274907,2539094.37477054 1181134.07701214,2539094.37477054 1181134.07701214)), MULTIPOLYGON(((2539102.56950579 1181128.03878617,2539101.27560022 1181139.2526344,2539111.19554289 1181140.11523811,2539111.62684475 1181134.07701214,2539111.62684475 1181134.07701214,2539102.56950579 1181128.03878617))), MULTIPOINT((2539076.69139448 1181128.47008802)))",
        )

        # Permit Request to Classify with mixed objects with lots of text for print demo
        permit_request7 = models.PermitRequest.objects.create(
            status=models.PermitRequest.STATUS_PROCESSING,
            administrative_entity=demo_administrative_entity,
            author=demo_author,
            is_public=True,
        )
        # Validations with long text
        models.PermitRequestValidation.objects.get_or_create(
            permit_request=permit_request7,
            department=department,
            validation_status=models.PermitRequestValidation.STATUS_APPROVED,
            comment_before=demo_small_text,
            comment_during=demo_small_text,
            comment_after=demo_small_text,
        )
        models.PermitRequestValidation.objects.get_or_create(
            permit_request=permit_request7,
            department=models.PermitDepartment.objects.get(group__name="validator-2"),
            validation_status=models.PermitRequestValidation.STATUS_APPROVED,
            comment_before=demo_small_text,
            comment_during=demo_small_text,
            comment_after=demo_small_text,
        )

        models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request7, works_object_type=demo_works_object_type
        )

        models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request7,
            works_object_type=demo_works_object_type_no_validation_document,
        )

        models.PermitRequestGeoTime.objects.create(
            permit_request=permit_request7,
            starts_at=timezone.now(),
            ends_at=timezone.now(),
            geom="GEOMETRYCOLLECTION(MULTIPOLYGON(((2539078 1181121, 2539092 1181084, 2539118 1181111, 2539099 1181105, 2539078 1181121))))",
        )

        # Amend propertie with long text
        amend_property_1 = models.PermitRequestAmendProperty.objects.create(
            name="Commentaire interne",
            is_visible_by_author=False,
        )
        amend_property_1.works_object_types.set(
            [demo_works_object_type, demo_works_object_type_no_validation_document]
        )
        amend_property_2 = models.PermitRequestAmendProperty.objects.create(
            name="Commentaire visible par le requérant",
            is_visible_by_author=True,
        )
        amend_property_2.works_object_types.set(
            [demo_works_object_type, demo_works_object_type_no_validation_document]
        )
        works_object_type_choice_1 = models.WorksObjectTypeChoice.objects.get(
            permit_request=permit_request7,
            works_object_type=demo_works_object_type,
        )
        works_object_type_choice_2 = models.WorksObjectTypeChoice.objects.get(
            permit_request=permit_request7,
            works_object_type=demo_works_object_type_no_validation_document,
        )
        models.PermitRequestAmendPropertyValue.objects.create(
            property=amend_property_1,
            works_object_type_choice=works_object_type_choice_1,
            value=demo_small_text,
        )
        models.PermitRequestAmendPropertyValue.objects.create(
            property=amend_property_1,
            works_object_type_choice=works_object_type_choice_2,
            value=demo_small_text,
        )
        models.PermitRequestAmendPropertyValue.objects.create(
            property=amend_property_2,
            works_object_type_choice=works_object_type_choice_1,
            value=demo_small_text,
        )
        models.PermitRequestAmendPropertyValue.objects.create(
            property=amend_property_2,
            works_object_type_choice=works_object_type_choice_2,
            value=demo_small_text,
        )

        # Set default values for properties
        for prop in models.WorksObjectProperty.objects.all():
            for works_object_type_choice in [
                works_object_type_choice_1,
                works_object_type_choice_2,
            ]:
                if prop.input_type == models.WorksObjectProperty.INPUT_TYPE_DATE:
                    models.WorksObjectPropertyValue.objects.create(
                        property=prop,
                        works_object_type_choice=works_object_type_choice,
                        value={"val": "01.01.2021"},
                    )
                if prop.input_type == models.WorksObjectProperty.INPUT_TYPE_ADDRESS:
                    models.WorksObjectPropertyValue.objects.create(
                        property=prop,
                        works_object_type_choice=works_object_type_choice,
                        value={"val": "Place pestalozzi 2, 1400 Yverdon-les-Bains"},
                    )
                if prop.input_type == models.WorksObjectProperty.INPUT_TYPE_CHECKBOX:
                    models.WorksObjectPropertyValue.objects.create(
                        property=prop,
                        works_object_type_choice=works_object_type_choice,
                        value={"val": True},
                    )
                if prop.input_type == models.WorksObjectProperty.INPUT_TYPE_NUMBER:
                    models.WorksObjectPropertyValue.objects.create(
                        property=prop,
                        works_object_type_choice=works_object_type_choice,
                        value={"val": 42},
                    )
                if prop.input_type == models.WorksObjectProperty.INPUT_TYPE_LIST_SINGLE:
                    models.WorksObjectPropertyValue.objects.create(
                        property=prop,
                        works_object_type_choice=works_object_type_choice,
                        value={"val": "Oui"},
                    )
                if (
                    prop.input_type
                    == models.WorksObjectProperty.INPUT_TYPE_LIST_MULTIPLE
                ):
                    models.WorksObjectPropertyValue.objects.create(
                        property=prop,
                        works_object_type_choice=works_object_type_choice,
                        value={"val": "Le bon choix"},
                    )
                if (
                    prop.input_type == models.WorksObjectProperty.INPUT_TYPE_TEXT
                    or prop.input_type == models.WorksObjectProperty.INPUT_TYPE_REGEX
                    or prop.input_type == models.WorksObjectProperty.INPUT_TYPE_TITLE
                ):
                    models.WorksObjectPropertyValue.objects.create(
                        property=prop,
                        works_object_type_choice=works_object_type_choice,
                        value={"val": demo_small_text},
                    )

    def create_geom_layer_entity(self):

        models.GeomLayer.objects.create(
            layer_name="Parcelle",
            description="Démo parcelle",
            source_id="1234",
            source_subid="9876",
            external_link="https://www.osm.org",
            geom="SRID=2056;MultiPolygon(((2526831.16912443 1159820.00193672, 2516148.68477727 1198947.70623155, 2551053.08130695 1201183.5750484, 2560741.84617995 1166651.82332153, 2526831.16912443 1159820.00193672)))",
        )

        models.GeomLayer.objects.create(
            layer_name="Archéologie",
            description="Démo archéologie",
            source_id="1234",
            source_subid="9876",
            external_link="https://www.osm.org",
            geom="SRID=2056;MultiPolygon(((2526831.16912443 1159820.00193672, 2516148.68477727 1198947.70623155, 2551053.08130695 1201183.5750484, 2560741.84617995 1166651.82332153, 2526831.16912443 1159820.00193672)))",
        )

    def setup_homepage(self):
        config.APPLICATION_TITLE = "Démo Geocity"
        config.APPLICATION_SUBTITLE = "Simplifiez votre administration"
        config.APPLICATION_DESCRIPTION = """<p><b>Essayez l'application à l'aide des différents comptes et rôles (utilisateur / mot de passe):</b></p>
        <p>Utilisateur standard: user / demo</p>
        <p>Pilote (secréatariat): pilot / demo</p>
        <p>Validateur: validator / demo</p>
        <p>Validateur 2: validator-2 / demo</p>
        <p>Intégrateur 2: integrator / demo</p>
        <p>Utilisateur: admin / demo</p>
        <p>Consultez les emails générés par l'application:</p>
        => <a href="https://mailhog.geocity.ch" target="_blank">Boîte mail de demo<a/>
        """

    def create_document_types(self, wot):
        document_types = [
            (
                "{} Parent #1".format(wot.pk),
                wot,
                ["{} Child #1.{}".format(wot.pk, i) for i in range(1, 4)],
            ),
            (
                "{} Parent #2".format(wot.pk),
                wot,
                ["{} Child #2.{}".format(wot.pk, i) for i in range(1, 5)],
            ),
        ]

        for document_type in document_types:
            name, work_object_type, children = document_type
            parent = models.ComplementaryDocumentType.objects.create(
                name=name, work_object_types=work_object_type, parent=None
            )

            for child in children:
                models.ComplementaryDocumentType.objects.create(
                    name=child, work_object_types=None, parent=parent
                )


demo_long_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
sunt in culpa qui officia deserunt mollit anim id est laborum.
Section 1.10.32 of de Finibus Bonorum et Malorum, written by Cicero in 45 BC

Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa
quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas
sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.
Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi
tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem
ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea
voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?
1914 translation by H. Rackham

But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a
complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness.
No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally
encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it
is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example,
which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a
man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?
Section 1.10.33 of de Finibus Bonorum et Malorum, written by Cicero in 45 BC

At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos
dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt
mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore,
cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est,
omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae
sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur
aut perferendis doloribus asperiores repellat.
1914 translation by H. Rackham

On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure
of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to
those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases
are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being
able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims
of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted.
The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures,
or else he endures pains to avoid worse pains.
"""

demo_medium_text = """
On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure
of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to
those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases
are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being
able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims
of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted.
The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures,
or else he endures pains to avoid worse pains"""

demo_small_text = """
On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure
of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to
those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases
are perfectly simple and easy to distinguish."""
