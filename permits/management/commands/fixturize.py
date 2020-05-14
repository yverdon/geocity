from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core import management
from django.core.management.base import BaseCommand
from django.db import connection, transaction

from gpf import models as gpf_models

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
    #management.call_command("loaddata", "db.json", stdout=StringIO())


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Resetting database...")
        reset_db()
        self.stdout.write("Creating users...")
        self.create_users()

    def create_users(self):
        user = User.objects.create_user(username='admin', password='admin', is_staff=True, is_superuser=True)
        gpf_models.Actor.objects.create(user=user, email="admin@localhost")
        self.stdout.write("admin / admin")

        user = User.objects.create_user(username='user', password='admin')
        gpf_models.Actor.objects.create(user=user, email="user@localhost")
        self.stdout.write("user / admin")

        self.create_user('secretariat-yverdon', 'Secrétariat Yverdon', 'Démo Yverdon')
        self.stdout.write("secretariat-yverdon / admin")

        self.create_user('secretariat-lausanne', 'Secrétariat Lausanne', 'Démo Lausanne')
        self.stdout.write("secretariat-lausanne / admin")

        admin = User.objects.get(username='admin')
        admin.set_password('admin')
        admin.save()
        self.stdout.write("admin / admin")

    def create_user(self, username, group_name, administrative_entity_name):
        administrative_entity, created = gpf_models.AdministrativeEntity.objects.get_or_create(
            name=administrative_entity_name, defaults={'ofs_id': 0}
        )
        group, created = Group.objects.get_or_create(name=group_name)
        user = User.objects.create_user(username=username, password='admin')
        user.groups.set([group])
        gpf_models.Actor.objects.create(user=user, email=f"{username}@localhost")
        gpf_models.Department.objects.create(
            group=group, is_validator=False, is_admin=False, is_archeologist=False,
            administrative_entity=administrative_entity
        )

        return user
