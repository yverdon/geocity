from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core import management
from django.core.management.base import BaseCommand
from django.db import connection, transaction

from permits import models

User = get_user_model()


def reset_db():
    """
   Reset database to a blank state by removing all the tables and recreating them.
    """
    with connection.cursor() as cursor:
        cursor.execute("select tablename from pg_tables where schemaname = 'public'")
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

    def create_users(self):
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
            address="Rue du Pont",
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
            first_name="Utilisateur",
            last_name="Externe",)
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
        user = self.create_user('secretariat-yverdon', 'Secrétariat Yverdon', 'Démo Yverdon')
        user.user_permissions.set(secretariat_permissions)
        self.stdout.write("secretariat-yverdon / admin")

        user = self.create_user('secretariat-lausanne', 'Secrétariat Lausanne', 'Démo Lausanne')
        user.user_permissions.set(secretariat_permissions)
        self.stdout.write("secretariat-lausanne / admin")

        user = self.create_user('validator-yverdon', 'Validateur Yverdon', 'Démo Yverdon', is_default_validator=True)
        Group.objects.get(name="Validateur Yverdon").permissions.add(
            Permission.objects.get(codename='validate_permit_request', content_type=permit_request_ct)
        )
        self.stdout.write("validator-yverdon / admin")

        user = self.create_user('eaux-yverdon', 'Service des eaux Yverdon', 'Démo Yverdon')
        Group.objects.get(name="Service des eaux Yverdon").permissions.add(
            Permission.objects.get(codename='validate_permit_request', content_type=permit_request_ct)
        )
        self.stdout.write("eaux-yverdon / admin")

    def create_user(self, username, group_name, administrative_entity_name, is_default_validator=False):
        administrative_entity, created = models.PermitAdministrativeEntity.objects.get_or_create(
            name=administrative_entity_name, defaults={
                'ofs_id': 0,
                'link': 'https://mapnv.ch',
                'title_signature_1': 'Marcel Dupond',
                'title_signature_2': 'Gérard Personne',
                }
        )

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
            "width": models.WorksObjectProperty.objects.create(name="Largeur [m]", input_type="number", is_mandatory=True),
            "height": models.WorksObjectProperty.objects.create(name="Hauteur [m]", input_type="number", is_mandatory=True),
            "plan": models.WorksObjectProperty.objects.create(name="Plan de situation", input_type="file", is_mandatory=True),
        }
        objects = [
            ("Jardin d'hiver chauffé", properties["width"], properties["height"]),
            ("Barbecues, fours à pain ou pizza", properties["width"], properties["height"]),
            ("Avant-toits", properties["width"], properties["height"], properties["plan"])
        ]
        works_types = [
            ("Événement sur domaine public", [
                ("Événement commercial", properties["plan"]),
                ("Événement culturel", properties["plan"])
            ]),
            ("Démolition", objects),
            ("Construction", objects),
        ]
        administrative_entity = models.PermitAdministrativeEntity.objects.get(name="Démo Yverdon")

        for works_type, objs in works_types:
            works_type_obj = models.WorksType.objects.create(name=works_type)
            models.PermitActorType.objects.create(
                type=models.ACTOR_TYPE_OTHER,
                works_type=works_type_obj,
            )

            for works_obj, *props in objs:
                works_obj_obj = models.WorksObject.objects.create(name=works_obj)
                works_object_type = models.WorksObjectType.objects.create(works_type=works_type_obj, works_object=works_obj_obj)
                works_object_type.administrative_entities.add(administrative_entity)
                for prop in props:
                    prop.works_object_types.add(works_object_type)
