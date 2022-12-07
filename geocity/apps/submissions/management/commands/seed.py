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

from geocity import settings
from geocity.apps.accounts.models import *
from geocity.apps.accounts.users import get_integrator_permissions
from geocity.apps.forms.models import *
from geocity.apps.reports.models import *
from geocity.apps.submissions.models import *


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
        # with transaction.atomic():
        #     self.stdout.write("Creating sites...")
        #     self.setup_sites()
        #     self.stdout.write("Creating users...")
        #     self.create_users()
        #     self.stdout.write("Creating form categories")
        #     self.create_form_categories()
        #     self.stdout.write("Creating demo submission...")
        #     self.create_submission()
        #     self.stdout.write("Creating template customizations...")
        #     self.create_template_customization()
        #     self.stdout.write("Configurating template customizations...")
        #     self.setup_homepage()
        #     self.stdout.write("Setting site integrator for selected configurations...")
        #     self.setup_integrator()
        #     self.stdout.write("Fixturize succeed!")

    entities = [
        "first_entity",
        "second_entity",
        "third_entity",
        "fourth_entity",
        "fifth_entity",
    ]
    integrators = [
        "first_integrator",
        "second_integrator",
        "third_integrator",
        "fourth_integrator",
        "fifth_integrator",
    ]
    geoms = [
        "SRID=2056;MultiPolygon (((2538391 1176432, 2538027 1178201, 2538485 1178804, 2537777 1179199, 2536748 1178450, 2536123 1179647, 2537382 1180593, 2537143 1181623, 2538651 1183257, 2540368 1183236, 2541252 1181093, 2541460 1180458, 2540160 1179543, 2540097 1178877, 2538391 1176432)))",
        "SRID=2056;MultiPolygon (((2543281 1184952, 2542053 1186731, 2541148 1186887, 2538214 1186367, 2537195 1184609, 2537153 1183330, 2537757 1182653, 2539317 1182404, 2543281 1184952)))",
        "SRID=2056;MultiPolygon (((2533045 1151566, 2533789 1154840, 2538236 1155380, 2541064 1154989, 2541790 1157408, 2540934 1160087, 2543074 1161259, 2546553 1159715, 2545399 1156329, 2542757 1155361, 2542348 1153798, 2542497 1152347, 2540692 1150617, 2535855 1152105, 2533045 1151566)),((2529938 1157110, 2529789 1160329, 2532245 1161557, 2532580 1160273, 2530831 1158934, 2530757 1157259, 2529938 1157110)))",
        "SRID=2056;MultiPolygon (((2553381 1146430, 2553679 1145798, 2553660 1145500, 2554777 1145296, 2555502 1145965, 2554870 1146617, 2555335 1147398, 2555037 1147417, 2554311 1146803, 2553418 1146840, 2553269 1146524, 2553381 1146430)))",
        "SRID=2056;MultiPolygon (((2538391 1176432, 2538027 1178201, 2538485 1178804, 2537777 1179199, 2536748 1178450, 2536123 1179647, 2537382 1180593, 2537143 1181623, 2538651 1183257, 2540368 1183236, 2541252 1181093, 2541460 1180458, 2540160 1179543, 2540097 1178877, 2538391 1176432)))",
    ]
    ofs_ids = [5938, 5938, 5586, 5890, 5938]

    def setup_necessary_default_site(self):
        Site.objects.get_or_create(domain=settings.DEFAULT_SITE, name="default site")

    def setup_sites(self, entities):
        for entity in entities:
            domain = f"{entity}.localhost"
            Site.objects.get_or_create(domain=domain, name=entity)

    def setup_integrator(self, integrators, entities):
        for idx, integrator in enumerate(integrators):
            integrator = Group.objects.get(name=integrator)
            AdministrativeEntity.objects.update(integrator=integrator)
            FormCategory.objects.update(integrator=integrator)
            Form.objects.update(integrator=integrator)
            ContactType.objects.update(integrator=integrator)
            ComplementaryDocumentType.objects.update(integrator=integrator)
            SubmissionAmendField.objects.update(integrator=integrator)

            # 1 integrator per site
            SiteProfile.objects.filter(site__name=entities[idx]).update(
                integrator=integrator
            )

    def create_administrative_entity(self, entity, ofs_id, geom):
        name = f"Démo {entity}"
        administrative_entity = AdministrativeEntity.objects.create(
            name=name,
            ofs_id=ofs_id,
            link="https://mapnv.ch",
            archive_link="https://mapnv.ch",
            geom=geom,
        )

        administrative_entity.tags.add(entity)
        administrative_entity.sites.add(Site.objects.get(name=entity))
        administrative_entity.sites.add(Site.objects.get(name="default site"))
        return administrative_entity

    # TODO: Do the same for super user and user
    def create_user_superuser(self, entity):
        email = f"{entity}-squad+admin@ylb.ch"
        username = f"{entity}-superuser"
        user = User.objects.create_user(
            email=email,
            first_name=username,
            last_name="Demo",
            username=username,
            password="demo",
            is_staff=True,
            is_superuser=True,
        )

        self.create_user_profile(self, user, entity)

    # /////////////////////////////////////
    # User integrator
    # /////////////////////////////////////

    def setup_user_integrator(self, entity, user_iteration, administrative_entity):
        # Define username
        username = f"{entity}-integrator-{user_iteration}"

        # Define email
        email = f"{entity}-squad+integrator-{user_iteration}@ylb.ch"

        # Create user
        user = self.create_user(self, username, email)

        # Create user profile
        self.create_user_profile(self, user, entity)

        # Create group and user in it
        group = self.create_group(username)
        user.groups.set([group])

        # Create permit_department
        self.create_permit_department(
            group,
            administrative_entity,
            is_default_validator=True,
            is_integrator_admin=True,
            is_staff=True,
        )

        # Set permissions
        permissions = get_integrator_permissions()
        group.permissions.set(permissions)

    # /////////////////////////////////////
    # User pilot
    # /////////////////////////////////////

    def setup_user_pilot(self, entity, user_iteration, administrative_entity):
        # Define username
        username = f"{entity}-pilot-{user_iteration}"

        # Define email
        email = f"{entity}-squad+pilot-{user_iteration}@ylb.ch"

        # Create user
        user = self.create_user(self, username, email)

        # Create user profile
        self.create_user_profile(self, user, entity)

        # Create group and user in it
        group = self.create_group(username)
        user.groups.set([group])

        # Create permit_department
        self.create_permit_department(group, administrative_entity)

        # Set permissions
        permissions = self.get_pilot_permissions()
        group.permissions.set(permissions)

    def get_pilot_permissions(self):
        secretariat_permissions = Permission.objects.filter(
            codename__in=[
                "amend_submission",
                "classify_submission",
            ],
            content_type=self.submission_ct,
        )

        secretariat_permissions_reports = Permission.objects.filter(
            codename__in=[
                "can_generate_pdf",
            ],
            content_type=self.reports_request_ct,
        )

        permissions = secretariat_permissions.union(secretariat_permissions_reports)
        return permissions

    # /////////////////////////////////////
    # User validator
    # /////////////////////////////////////

    def setup_user_validator(self, entity, user_iteration, administrative_entity):
        # Define username
        username = f"{entity}-validator-{user_iteration}"

        # Define email
        email = f"{entity}-squad+validator-{user_iteration}@ylb.ch"

        # Create user
        user = self.create_user(self, username, email)

        # Create user profile
        self.create_user_profile(self, user, entity)

        # Create group and user in it
        group = self.create_group(username)
        user.groups.set([group])

        # Create permit_department
        self.create_permit_department(
            group, administrative_entity, is_validator=True, is_default_validator=True
        )

        # Set permissions
        permissions = self.get_validator_permissions()
        group.permissions.set(permissions)

    def get_validator_permissions(self):
        permissions = Permission.objects.get(
            codename="validate_submission", content_type=self.submission_ct
        )
        return permissions

    # /////////////////////////////////////
    # Functions
    # /////////////////////////////////////

    def create_user(self, username, email, is_staff=False):
        user = User.objects.create_user(
            email=email,
            first_name=username,
            last_name="Demo",
            username=username,
            password="demo",
            is_staff=is_staff,
        )

        return user

    def create_user_profile(self, user, entity):
        UserProfile.objects.create(
            user=user,
            address="Place Pestalozzi 2",
            zipcode=1234,
            city=entity,
            phone_first="000 00 00 00",
            phone_second="000 00 00 00",
        )

    def create_group(self, username):
        group = Group.objects.get_or_create(name=username)
        return group

    def create_permit_department(
        self,
        group,
        administrative_entity,
        is_validator=False,
        is_integrator_admin=False,
        is_backoffice=False,
        is_default_validator=False,
    ):
        PermitDepartment.objects.create(
            group=group,
            administrative_entity=administrative_entity,
            is_validator=is_validator,
            is_integrator_admin=is_integrator_admin,
            is_backoffice=is_backoffice,
            is_default_validator=is_default_validator,
        )

    def create_users(self, entities, ofs_ids, geoms):
        """For each administrative entity, create :
        - Administrative entity
        - 1 super user
        - 3 integrators
        - 5 pilots
            - With permissions
            - With group
        - 6 validators
        - 8 users
        """
        # Store ContentType.objects for model Submission and Report to prevent requests
        self.submission_ct = ContentType.objects.get_for_model(Submission)
        self.reports_request_ct = ContentType.objects.get_for_model(Report)

        for idx, entity in enumerate(entities):

            # Create administrative entity
            administrative_entity = self.create_administrative_entity(
                entity, ofs_ids[idx], geoms[idx]
            )

            # Create superuser
            self.create_user_superuser(entity)
            self.stdout.write(f"Create superuser for entity {entity}")

            # Create integrators
            user_iterations = 3
            for user_iteration in range(user_iterations):
                self.create_user_integrator(entity, user_iteration)
            self.stdout.write(f"Create {user_iterations} integrators for {entity}")

            # Create pilots
            user_iterations = 5
            for user_iteration in range(user_iterations):
                self.create_user_pilot(entity, user_iteration, administrative_entity)
            self.stdout.write(f"Create {user_iterations} pilots for {entity}")

            # Create validators
            user_iterations = 6
            for user_iteration in range(user_iterations):
                self.create_user_validator(
                    entity, user_iteration, administrative_entity
                )
            self.stdout.write(f"Create {user_iterations} validators for {entity}")

            # Create users
            user_iterations = 8
            for user_iteration in range(user_iterations):
                self.create_user(entity, user_iteration)
            self.stdout.write(f"Create {user_iterations} users for {entity}")
