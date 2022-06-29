import re
import unicodedata
from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core import management
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.utils import timezone

from geomapshark import settings
from permits import admin, models


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
            self.stdout.write("Setup base Site object...")
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
            self.create_permit_site()
            self.setup_homepage()
            self.stdout.write("Setting up dev homepage...")
            self.stdout.write("Fixturize succeed.")

    def setup_site(self):
        # Default site generated by django's post migration hook
        site = Site.objects.get()
        site.name = "localhost"
        site.domain = "localhost"
        site.save()
        # New site to demonstrate administrative entity filtering by subdomain filter
        Site.objects.create(domain="yverdon.localhost", name="yverdon")
        Site.objects.create(domain="grandson.localhost", name="grandson")
        Site.objects.create(domain="vevey.localhost", name="vevey")
        Site.objects.create(domain="lausanne.localhost", name="lausanne")

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
            first_name="Super",
            last_name="Admin",
            username="admin",
            password="admin",
            is_staff=True,
            is_superuser=True,
        )
        self.stdout.write("admin / admin")

        models.PermitAuthor.objects.create(
            user=user,
            address="Rue du test",
            zipcode=1234,
            city="Métropole",
            phone_first="000 00 00 00",
            phone_second="000 00 00 00",
        )

        user = User.objects.create_user(
            username="user",
            password="admin",
            email=f"yverdon-squad+user@liip.ch",
            first_name="Antoine",
            last_name="Ducommun",
        )
        models.PermitAuthor.objects.create(
            user=user,
            address="Rue du Port",
            zipcode=1234,
            city="Mégalopole",
            phone_first="000 00 00 00",
            phone_second="000 00 00 00",
        )
        self.stdout.write("user / admin")

        permit_request_ct = ContentType.objects.get_for_model(models.PermitRequest)
        secretariat_permissions = Permission.objects.filter(
            codename__in=["amend_permit_request", "classify_permit_request"],
            content_type=permit_request_ct,
        )
        user = self.create_user(
            "secretariat-yverdon",
            "Secrétariat Yverdon",
            administrative_entity_yverdon,
            email="yverdon-squad+secretariat-yverdon@liip.ch",
        )
        user.user_permissions.set(secretariat_permissions)
        self.stdout.write("secretariat-yverdon / admin")

        user = self.create_user(
            "secretariat-grandson",
            "Secrétariat Grandson",
            administrative_entity_grandson,
            email="yverdon-squad+secretariat-grandson@liip.ch",
        )
        user.user_permissions.set(secretariat_permissions)
        self.stdout.write("secretariat-grandson / admin")

        secretary_groups = Group.objects.filter(
            name__in=["Secrétariat Yverdon", "Secrétariat Grandson"]
        )
        department = models.PermitDepartment.objects.filter(
            group__in=secretary_groups
        ).update(is_backoffice=True)

        user = self.create_user(
            "validator-yverdon",
            "Validateur Yverdon",
            administrative_entity_yverdon,
            is_default_validator=True,
            email="yverdon-squad+validator-yverdon@liip.ch",
        )
        Group.objects.get(name="Validateur Yverdon").permissions.add(
            Permission.objects.get(
                codename="validate_permit_request", content_type=permit_request_ct
            )
        )

        validator_group = Group.objects.get(name="Validateur Yverdon")
        departement = models.PermitDepartment.objects.get(group=validator_group)
        departement.is_validator = True
        departement.save()

        self.stdout.write("validator-yverdon / admin")

        user = self.create_user(
            "eaux-yverdon",
            "Service des eaux Yverdon",
            administrative_entity_yverdon,
            email="yverdon-squad+eaux-yverdon@liip.ch",
        )
        Group.objects.get(name="Service des eaux Yverdon").permissions.add(
            Permission.objects.get(
                codename="validate_permit_request", content_type=permit_request_ct
            )
        )
        self.stdout.write("eaux-yverdon / admin")

        user = self.create_user(
            "integrator-yverdon",
            "Integrator Yverdon",
            administrative_entity_yverdon,
            is_default_validator=True,
            is_integrator_admin=True,
            is_staff=True,
            email="yverdon-squad+integrator-yverdon@liip.ch",
        )

        permits_permissions = Permission.objects.filter(
            content_type__app_label="permits",
            content_type__model__in=admin.INTEGRATOR_PERMITS_MODELS_PERMISSIONS,
        )

        other_permissions = Permission.objects.filter(
            codename__in=admin.OTHER_PERMISSIONS_CODENAMES
        )
        # set the required permissions for the integrator group
        Group.objects.get(name="Integrator Yverdon").permissions.set(
            permits_permissions.union(other_permissions)
        )
        self.stdout.write("integrator-yverdon / admin")

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
            first_name="Mon Prénom",
            last_name="Mon Nom",
            username=username,
            password="admin",
            is_staff=is_staff,
        )
        user.groups.set([group])
        models.PermitAuthor.objects.create(
            user=user,
            address="Rue du Lac",
            zipcode=1234,
            city="Ville",
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
            "comment": models.WorksObjectProperty.objects.create(
                name="Commentaire", input_type="text", is_mandatory=True, order=5
            ),
            "width": models.WorksObjectProperty.objects.create(
                name="Largeur [m]", input_type="number", is_mandatory=True, order=1
            ),
            "height": models.WorksObjectProperty.objects.create(
                name="Hauteur [m]", input_type="number", is_mandatory=True, order=2
            ),
            "plan": models.WorksObjectProperty.objects.create(
                name="Plan de situation", input_type="file", is_mandatory=True, order=3
            ),
            "adresse": models.WorksObjectProperty.objects.create(
                name="Adresse", input_type="address", is_mandatory=True
            ),
        }
        objects = [
            (
                "Jardin d'hiver chauffé",
                properties["width"],
                properties["height"],
                properties["comment"],
                properties["adresse"],
            ),
            (
                "Barbecues, fours à pain ou pizza",
                properties["width"],
                properties["height"],
                properties["comment"],
                properties["adresse"],
            ),
            (
                "Avant-toits",
                properties["width"],
                properties["height"],
                properties["plan"],
                properties["comment"],
                properties["adresse"],
            ),
        ]
        works_types = [
            (
                "Procédés de réclame",
                [
                    ("Enseigne lumnineuse", properties["comment"]),
                    ("Panneau", properties["comment"]),
                ],
            ),
            ("Démolition", objects),
            ("Construction", objects),
        ]
        administrative_entity_yverdon = models.PermitAdministrativeEntity.objects.get(
            name="Démo Yverdon"
        )
        administrative_entity_grandson = models.PermitAdministrativeEntity.objects.get(
            name="Démo Grandson"
        )
        administrative_entity_lausanne = models.PermitAdministrativeEntity.objects.get(
            name="Démo Lausanne"
        )
        administrative_entity_vevey = models.PermitAdministrativeEntity.objects.get(
            name="Démo Vevey"
        )

        for works_type, objs in works_types:
            works_type_obj = models.WorksType.objects.create(name=works_type)
            works_type_obj.tags.add(unaccent(works_type))
            models.PermitActorType.objects.create(
                type=models.ACTOR_TYPE_OTHER,
                works_type=works_type_obj,
            )

            for works_obj, *props in objs:
                works_obj_obj, created = models.WorksObject.objects.get_or_create(
                    name=works_obj
                )
                works_object_type = models.WorksObjectType.objects.create(
                    works_type=works_type_obj,
                    works_object=works_obj_obj,
                    is_public=True,
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
        )

        wot_choice2 = models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request2,
            works_object_type=demo_works_object_type_no_validation_document,
        )

        models.WorksObjectPropertyValue.objects.create(
            property=demo_works_object_type.properties.first(),
            works_object_type_choice=wot_choice2,
            value={
                "val": "Ceci est un commentaire de démonstration pour demande {}".format(
                    permit_request2.id
                )
            },
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
        )

        wot_choice3_1 = models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request3, works_object_type=demo_works_object_type
        )

        models.WorksObjectPropertyValue.objects.create(
            property=demo_works_object_type.properties.first(),
            works_object_type_choice=wot_choice3_1,
            value={
                "val": "Ceci est un commentaire de démonstration pour demande {}_{}".format(
                    permit_request3.id, wot_choice3_1.id
                )
            },
        )

        wot_choice3_2 = models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request3,
            works_object_type=demo_works_object_type_no_validation_document,
        )

        models.WorksObjectPropertyValue.objects.create(
            property=demo_works_object_type.properties.first(),
            works_object_type_choice=wot_choice3_2,
            value={
                "val": "Ceci est un commentaire de démonstration pour demande {}_{}".format(
                    permit_request3.id, wot_choice3_2.id
                )
            },
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

    def create_permit_site(self):
        models.PermitSite.objects.create(
            templatename="geocity",
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

        models.PermitSite.objects.create(
            templatename="city",
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
