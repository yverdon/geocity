from io import StringIO
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core import management
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.utils import timezone

from permits import models

User = get_user_model()


def reset_db():
    """
   Reset database to a blank state by removing all the tables and recreating them.
    """
    with connection.cursor() as cursor:

        cursor.execute("select tablename from pg_tables where schemaname = 'geocity' or schemaname = 'public'")
        tables = [row[0] for row in cursor.fetchall() if row[0] not in {'spatial_ref_sys'}]
        # Can't use query parameters here as they'll add single quotes which are not
        # supported by postgres
        for table in tables:
            cursor.execute('drop table "' + table + '" cascade')

    # Call migrate so that post-migrate hooks such as generating a default Site object
    # are run
    management.call_command("migrate", "--noinput", stdout=StringIO())


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Resetting database...")
        reset_db()
        self.stdout.write("Creating users...")
        self.create_users()
        self.stdout.write("Creating works types and objs...")
        self.create_works_types()
        self.stdout.write("Creating demo permit...")
        self.create_permit()
        self.stdout.write("Creating dummy geometric entities...")
        self.create_geom_layer_entity()

    def create_users(self):

        administrative_entity_yverdon = models.PermitAdministrativeEntity.objects.create(
            name='Démo Yverdon',
            ofs_id=0,
            link='https://mapnv.ch',
            legal_document="administrative_entity_customization/demo-directive.pdf",
            general_informations="Prix par jour: 40CHF",
            archive_link='https://mapnv.ch',
            title_signature_1='Responsable Yverdon 1',
            title_signature_2='Responsable Yverdon 2',
            geom="SRID=2056;MultiPolygon (((2538391 1176432, 2538027 1178201, 2538485 1178804, 2537777 1179199, 2536748 1178450, 2536123 1179647, 2537382 1180593, 2537143 1181623, 2538651 1183257, 2540368 1183236, 2541252 1181093, 2541460 1180458, 2540160 1179543, 2540097 1178877, 2538391 1176432)))"
        )

        administrative_entity_grandson = models.PermitAdministrativeEntity.objects.create(
            name='Démo Grandson',
            ofs_id=0,
            link='https://mapnv.ch',
            legal_document="administrative_entity_customization/demo-directive.pdf",
            general_informations="Prix par jour: 45CHF",
            archive_link='https://mapnv.ch',
            title_signature_1='Responsable Grandson 1',
            title_signature_2='Responsable Grandson 2',
            geom="SRID=2056;MultiPolygon (((2543281 1184952, 2542053 1186731, 2541148 1186887, 2538214 1186367, 2537195 1184609, 2537153 1183330, 2537757 1182653, 2539317 1182404, 2543281 1184952)))"
        )

        user = User.objects.create_user(
            email=f"yverdon-squad+admin@liip.ch",
            first_name="Super",
            last_name="Admin",
            username='admin',
            password='admin',
            is_staff=True,
            is_superuser=True)
        models.PermitAuthor.objects.create(
            user=user,
            address="Rue du test",
            zipcode=1234,
            city="Métropole",
            phone_first="000 00 00 00",
            phone_second="000 00 00 00",
        )
        self.stdout.write("admin / admin")

        user = User.objects.create_user(
            username='user',
            password='admin',
            email=f"yverdon-squad+user@liip.ch",
            first_name="Antoine",
            last_name="Ducommun",)
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
            codename__in=['amend_permit_request', 'classify_permit_request'], content_type=permit_request_ct
        )
        user = self.create_user('secretariat-yverdon', 'Secrétariat Yverdon', administrative_entity_yverdon)
        user.user_permissions.set(secretariat_permissions)
        self.stdout.write("secretariat-yverdon / admin")

        user = self.create_user('secretariat-grandson', 'Secrétariat Grandson', administrative_entity_grandson)
        user.user_permissions.set(secretariat_permissions)
        self.stdout.write("secretariat-grandson / admin")

        user = self.create_user('validator-yverdon', 'Validateur Yverdon', administrative_entity_yverdon, is_default_validator=True)
        Group.objects.get(name="Validateur Yverdon").permissions.add(
            Permission.objects.get(codename='validate_permit_request', content_type=permit_request_ct)
        )
        self.stdout.write("validator-yverdon / admin")

        user = self.create_user('eaux-yverdon', 'Service des eaux Yverdon', administrative_entity_yverdon)
        Group.objects.get(name="Service des eaux Yverdon").permissions.add(
            Permission.objects.get(codename='validate_permit_request', content_type=permit_request_ct)
        )
        self.stdout.write("eaux-yverdon / admin")

        # Insert status choices from PermitRequest and insert status for adminsitrative_entity
        for status_value in models.PermitRequest.STATUS_CHOICES:
            choice, created = models.PermitWorkFlowStatus.objects.get_or_create(status=status_value[0], administrative_entity=administrative_entity_yverdon)
            choice, created = models.PermitWorkFlowStatus.objects.get_or_create(status=status_value[0], administrative_entity=administrative_entity_grandson)




    def create_user(self, username, group_name, administrative_entity, is_default_validator=False):

        group, created = Group.objects.get_or_create(name=group_name)
        user = User.objects.create_user(
            email=f"yverdon-squad+user@liip.ch",
            first_name="Mon Prénom",
            last_name="Mon Nom",
            username=username,
            password='admin')
        user.groups.set([group])
        models.PermitAuthor.objects.create(
            user=user,
            address="Rue du Lac",
            zipcode=1234,
            city="Ville",)
        models.PermitDepartment.objects.create(
            group=group, is_validator=False, is_admin=False, is_archeologist=False,
            administrative_entity=administrative_entity, is_default_validator=is_default_validator
        )

        return user

    def create_works_types(self):
        properties = {
            "comment": models.WorksObjectProperty.objects.create(name="Commentaire", input_type="text", is_mandatory=True),
            "width": models.WorksObjectProperty.objects.create(name="Largeur [m]", input_type="number", is_mandatory=True),
            "height": models.WorksObjectProperty.objects.create(name="Hauteur [m]", input_type="number", is_mandatory=True),
            "plan": models.WorksObjectProperty.objects.create(name="Plan de situation", input_type="file", is_mandatory=True),
        }
        objects = [
            ("Jardin d'hiver chauffé", properties["width"], properties["height"], properties["comment"]),
            ("Barbecues, fours à pain ou pizza", properties["width"], properties["height"], properties["comment"]),
            ("Avant-toits", properties["width"], properties["height"], properties["plan"],properties["comment"])
        ]
        works_types = [
            ("Procédés de réclame", [
                ("Enseigne lumnieuse", properties["comment"]),
                ("Panneau", properties["comment"])
            ]),
            ("Démolition", objects),
            ("Construction", objects),
        ]
        administrative_entity_yverdon = models.PermitAdministrativeEntity.objects.get(name="Démo Yverdon")
        administrative_entity_grandson = models.PermitAdministrativeEntity.objects.get(name="Démo Grandson")

        for works_type, objs in works_types:
            works_type_obj = models.WorksType.objects.create(name=works_type)
            models.PermitActorType.objects.create(
                type=models.ACTOR_TYPE_OTHER,
                works_type=works_type_obj,
            )

            for works_obj, *props in objs:
                works_obj_obj = models.WorksObject.objects.create(name=works_obj)
                works_object_type = models.WorksObjectType.objects.create(works_type=works_type_obj, works_object=works_obj_obj)
                works_object_type.administrative_entities.add(administrative_entity_yverdon)
                works_object_type.administrative_entities.add(administrative_entity_grandson)
                for prop in props:
                    prop.works_object_types.add(works_object_type)

    def create_permit(self):

        demo_user = User.objects.get(username="user")
        demo_author = models.PermitAuthor.objects.get(id=demo_user.id)
        demo_administrative_entity = models.PermitAdministrativeEntity.objects.get(name="Démo Yverdon")
        demo_works_object_type = models.WorksObjectType.objects.first()

        permit_request = models.PermitRequest.objects.create(
            status=models.PermitRequest.STATUS_DRAFT,
            administrative_entity=demo_administrative_entity,
            author=demo_author,
        )

        models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request,
            works_object_type=demo_works_object_type
        )

        models.PermitRequestGeoTime.objects.create(
            permit_request=permit_request,
            starts_at=timezone.now(),
            ends_at=timezone.now(),
            geom="GEOMETRYCOLLECTION(MULTILINESTRING((2539096.09997796 1181119.41274907,2539094.37477054 1181134.07701214,2539094.37477054 1181134.07701214)), MULTIPOLYGON(((2539102.56950579 1181128.03878617,2539101.27560022 1181139.2526344,2539111.19554289 1181140.11523811,2539111.62684475 1181134.07701214,2539111.62684475 1181134.07701214,2539102.56950579 1181128.03878617))), MULTIPOINT((2539076.69139448 1181128.47008802)))"
        )

    def create_geom_layer_entity(self):

        models.GeomLayer.objects.create(
            layer_name='Parcelle',
            description="Démo parcelle",
            source_id="1234",
            source_subid="9876",
            external_link="https://www.osm.org",
            geom="SRID=2056;MultiPolygon(((2526831.16912443 1159820.00193672, 2516148.68477727 1198947.70623155, 2551053.08130695 1201183.5750484, 2560741.84617995 1166651.82332153, 2526831.16912443 1159820.00193672)))",
        )

        models.GeomLayer.objects.create(
            layer_name='Archéologie',
            description="Démo archéologie",
            source_id="1234",
            source_subid="9876",
            external_link="https://www.osm.org",
            geom="SRID=2056;MultiPolygon(((2526831.16912443 1159820.00193672, 2516148.68477727 1198947.70623155, 2551053.08130695 1201183.5750484, 2560741.84617995 1166651.82332153, 2526831.16912443 1159820.00193672)))",
        )
