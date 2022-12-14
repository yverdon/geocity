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

# Change this import to change the data
from ..seed_data.example import *


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
        self.stdout.write("")
        self.stdout.write("")
        self.stdout.write("░██████╗███████╗███████╗██████╗░")
        self.stdout.write("██╔════╝██╔════╝██╔════╝██╔══██╗")
        self.stdout.write("╚█████╗░█████╗░░█████╗░░██║░░██║")
        self.stdout.write("░╚═══██╗██╔══╝░░██╔══╝░░██║░░██║")
        self.stdout.write("██████╔╝███████╗███████╗██████╔╝")
        self.stdout.write("╚═════╝░╚══════╝╚══════╝╚═════╝░")
        self.stdout.write("")
        self.stdout.write("")

        with transaction.atomic():
            self.stdout.write("Creating default site...")
            self.setup_necessary_default_site()
            for idx, (domain, entity) in enumerate(entities.items()):
                self.stdout.write(f"Entity : {entity}")
                self.stdout.write(" • Creating site...")
                self.setup_site(entity)
                self.stdout.write(" • Creating administrative entity...")
                administrative_entity = self.create_administrative_entity(
                    entity, ofs_ids[idx], geoms[idx]
                )
                self.stdout.write(" • Creating users...")
                integrator_group = self.create_users(
                    iterations, entity, domain, administrative_entity
                )
                self.stdout.write(" • Setting administrative_entity integrator...")
                self.setup_administrative_entity_integrator(
                    administrative_entity, integrator_group
                )
                self.stdout.write(" • Setting site integrator...")
                self.setup_site_integrator(entity)
                self.stdout.write(
                    " • Setting form, form categories and complementary document type..."
                )
                self.setup_form_and_form_categories(
                    form_categories,
                    integrator_group,
                    form_additional_information,
                    administrative_entity,
                )
            self.stdout.write("Seed succeed ✔")

    def setup_necessary_default_site(self):
        Site.objects.get_or_create(domain=settings.DEFAULT_SITE, name="default site")

    def setup_site(self, entity):
        domain = f"{entity}.localhost"
        Site.objects.get_or_create(domain=domain, name=entity)

    def create_users(self, iterations, entity, domain, administrative_entity):
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
        # Store ContentType.objects for model Submission and Report to prevent multiple requests
        self.submission_ct = ContentType.objects.get_for_model(Submission)
        self.reports_request_ct = ContentType.objects.get_for_model(Report)

        integrator_iterations = iterations.get("integrator_iterations")
        pilot_iterations = iterations.get("pilot_iterations")
        validator_iterations = iterations.get("validator_iterations")
        user_iterations = iterations.get("user_iterations")

        # Create superuser
        self.setup_user_superuser(entity, domain)

        # Create integrators
        for integrator_iteration in range(integrator_iterations):
            integrator_group = self.setup_user_integrator(
                entity, domain, integrator_iteration, administrative_entity
            )

        # Create pilots
        for pilot_iteration in range(pilot_iterations):
            self.setup_user_pilot(
                entity,
                domain,
                pilot_iteration,
                administrative_entity,
                integrator_group.pk,
            )

        # Create validators
        for validator_iteration in range(validator_iterations):
            self.setup_user_validator(
                entity,
                domain,
                validator_iteration,
                administrative_entity,
                integrator_group.pk,
            )

        # Create users
        for user_iteration in range(user_iterations):
            self.setup_user(entity, domain, user_iteration)

        return integrator_group

    def setup_site_integrator(self, entity):
        group = f"{entity}-integrator"
        integrator = Group.objects.get(name=group)
        # ComplementaryDocumentType.objects.update(integrator=integrator)
        # SubmissionAmendField.objects.update(integrator=integrator)

        # 1 integrator per site
        SiteProfile.objects.filter(site__name=entity).update(integrator=integrator)

    def setup_administrative_entity_integrator(
        self, administrative_entity, integrator_group
    ):
        # Setup administrative entity integrator
        administrative_entity.integrator = integrator_group
        administrative_entity.save()

    def setup_form_and_form_categories(
        self,
        form_categories,
        integrator_group,
        form_additional_information,
        administrative_entity,
    ):
        form_order = 0
        for form_category, objs in form_categories:
            form_category_obj = FormCategory.objects.create(
                name=form_category,
                integrator=integrator_group,
            )
            form_category_obj.tags.add(unaccent(form_category))
            ContactType.objects.create(
                type=CONTACT_TYPE_OTHER,
                form_category=form_category_obj,
                is_mandatory=False,
                integrator=integrator_group,
            )

            for form, *fields in objs:
                form_obj, form_order = self.create_form(
                    form,
                    form_category_obj,
                    form_additional_information,
                    form_order,
                    administrative_entity,
                    integrator_group,
                )

                self.create_document_types(form_obj, integrator_group)

                for order, field in enumerate(fields):
                    field = self.create_field(field, integrator_group)
                    self.create_form_field(field, form_obj, order)

        # Configure specific form in order to illustrate full potential of Geocity

        # No geom nor time
        for form in Form.objects.filter(
            category__name="Subventions (ex. de demande sans géométrie ni période temporelle)"
        ):
            form.has_geometry_point = False
            form.has_geometry_line = False
            form.has_geometry_polygon = False
            form.needs_date = False
            form.save()

        # Renewal reminder
        for form in Form.objects.filter(
            category__name="Stationnement (ex. de demande devant être prolongée)"
        ):
            form.has_geometry_point = True
            form.has_geometry_line = False
            form.has_geometry_polygon = False
            form.needs_date = True
            form.start_delay = 1
            form.permit_duration = 2
            form.expiration_reminder = True
            form.days_before_reminder = 5
            form.save()

    def create_form(
        self,
        form,
        form_category_obj,
        form_additional_information,
        form_order,
        administrative_entity,
        integrator_group,
    ):
        form_obj = Form.objects.create(
            name=form,
            category=form_category_obj,
            is_public=True,
            notify_services=True,
            document_enabled=True,
            publication_enabled=True,
            permanent_publication_enabled=True,
            services_to_notify=f"yverdon-squad+admin@liip.ch",
            additional_information=form_additional_information,
            order=form_order,
            integrator=integrator_group,
        )
        form_obj.administrative_entities.add(administrative_entity)
        form_order += 1

        return form_obj, form_order

    def create_document_types(self, form, integrator_group):
        document_types = [
            (
                "{} Parent #1".format(form.pk),
                form,
                ["{} Child #1.{}".format(form.pk, i) for i in range(1, 4)],
            ),
            (
                "{} Parent #2".format(form.pk),
                form,
                ["{} Child #2.{}".format(form.pk, i) for i in range(1, 5)],
            ),
        ]

        for document_type in document_types:
            name, form, children = document_type
            parent = ComplementaryDocumentType.objects.create(
                name=name, form=form, parent=None, integrator=integrator_group
            )

            for child in children:
                ComplementaryDocumentType.objects.create(
                    name=child, form=None, parent=parent
                )

    def create_field(self, field, integrator_group):
        # Defines possible fields for Field model
        integrator = integrator_group
        name = field.get("name")
        placeholder = field.get("placeholder", "")
        help_text = field.get("help_text", "")
        input_type = field.get("input_type")
        line_number_for_textarea = field.get("line_number_for_textarea", None)
        is_mandatory = field.get("is_mandatory", False)
        choices = field.get("choices", "")
        regex_pattern = field.get("regex_pattern", "")
        services_to_notify = field.get("services_to_notify", "")
        file_download = field.get("file_download", "")
        additional_searchtext_for_address_field = field.get(
            "additional_searchtext_for_address_field", ""
        )
        store_geometry_for_address_field = field.get(
            "store_geometry_for_address_field", False
        )
        is_public_when_permitrequest_is_public = field.get(
            "is_public_when_permitrequest_is_public", False
        )

        field, created = Field.objects.get_or_create(
            integrator=integrator,
            name=name,
            placeholder=placeholder,
            help_text=help_text,
            input_type=input_type,
            line_number_for_textarea=line_number_for_textarea,
            is_mandatory=is_mandatory,
            choices=choices,
            regex_pattern=regex_pattern,
            services_to_notify=services_to_notify,
            file_download=file_download,
            additional_searchtext_for_address_field=additional_searchtext_for_address_field,
            store_geometry_for_address_field=store_geometry_for_address_field,
            is_public_when_permitrequest_is_public=is_public_when_permitrequest_is_public,
        )
        return field

    def create_form_field(self, field, form_obj, order):
        FormField.objects.get_or_create(field=field, form=form_obj, order=order)

    def create_submissions(self):
        pass

    # /////////////////////////////////////
    # Functions used to make code DRY and readable
    # /////////////////////////////////////

    # /////////////////////////////////////
    # User superuser
    # /////////////////////////////////////

    def setup_user_superuser(self, entity, domain):
        # Define username
        username = f"{entity}-superuser"

        # Define email
        email = f"{entity}-squad+superuser@{domain}"

        # Create user
        user = self.create_user(
            username,
            email,
            is_staff=True,
            is_superuser=True,
        )

        # Create user profile
        self.create_user_profile(user, entity)

    # /////////////////////////////////////
    # User integrator
    # /////////////////////////////////////

    def setup_user_integrator(
        self, entity, domain, integrator_iteration, administrative_entity
    ):
        # Define username
        username = f"{entity}-integrator-{integrator_iteration}"

        # Define email
        email = f"{entity}-squad+integrator-{integrator_iteration}@{domain}"

        # Define group
        group = f"{entity}-integrator"

        # Create user
        user = self.create_user(username, email, is_staff=True)

        # Create user profile
        self.create_user_profile(user, entity)

        # Create group and user in it
        group = self.create_group(group)
        user.groups.set([group])

        # Create permit_department
        self.create_permit_department(
            group,
            administrative_entity,
            is_default_validator=True,
            is_integrator_admin=True,
            integrator_email_domains=domain,
        )

        # Set permissions
        permissions = get_integrator_permissions()
        group.permissions.set(permissions)
        return group

    # /////////////////////////////////////
    # User pilot
    # /////////////////////////////////////

    def setup_user_pilot(
        self, entity, domain, pilot_iteration, administrative_entity, integrator_group
    ):
        # Define username
        username = f"{entity}-pilot-{pilot_iteration}"

        # Define email
        email = f"{entity}-squad+pilot-{pilot_iteration}@{domain}"

        # Define group
        group = f"{entity}-pilot"

        # Create user
        user = self.create_user(username, email)

        # Create user profile
        self.create_user_profile(user, entity)

        # Create group and user in it
        group = self.create_group(group)
        user.groups.set([group])

        # Create permit_department
        self.create_permit_department(
            group, administrative_entity, integrator=integrator_group
        )

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

    def setup_user_validator(
        self,
        entity,
        domain,
        validator_iteration,
        administrative_entity,
        integrator_group,
    ):
        # Define username
        username = f"{entity}-validator-{validator_iteration}"

        # Define email
        email = f"{entity}-squad+validator-{validator_iteration}@{domain}"

        # Define group
        group = f"{entity}-validator"

        # Create user
        user = self.create_user(username, email)

        # Create user profile
        self.create_user_profile(user, entity)

        # Create group and user in it
        group = self.create_group(group)
        user.groups.set([group])

        # Create permit_department
        self.create_permit_department(
            group,
            administrative_entity,
            is_validator=True,
            is_default_validator=True,
            integrator=integrator_group,
        )

        # Set permissions
        permissions = self.get_validator_permissions()
        group.permissions.set([permissions])

    def get_validator_permissions(self):
        permissions = Permission.objects.get(
            codename="validate_submission", content_type=self.submission_ct
        )
        return permissions

    # /////////////////////////////////////
    # User
    # /////////////////////////////////////

    def setup_user(self, entity, domain, user_iteration):
        # Define username
        username = f"{entity}-user-{user_iteration}"

        # Define email
        email = f"{entity}-squad+user-{user_iteration}@{domain}"

        # Create user
        user = self.create_user(username, email)

        # Create user profile
        self.create_user_profile(user, entity)

    # /////////////////////////////////////
    # Functions
    # /////////////////////////////////////

    def create_user(self, username, email, is_staff=False, is_superuser=False):
        user = User.objects.create_user(
            email=email,
            first_name=username,
            last_name="Demo",
            username=username,
            password="demo",
            is_staff=is_staff,
            is_superuser=is_superuser,
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
        group, created = Group.objects.get_or_create(name=username)
        return group

    def create_permit_department(
        self,
        group,
        administrative_entity,
        is_validator=False,
        is_integrator_admin=False,
        is_backoffice=False,
        is_default_validator=False,
        integrator=0,
        integrator_email_domains="",
    ):
        PermitDepartment.objects.get_or_create(
            group=group,
            administrative_entity=administrative_entity,
            is_validator=is_validator,
            is_integrator_admin=is_integrator_admin,
            is_backoffice=is_backoffice,
            is_default_validator=is_default_validator,
            integrator=integrator,
            integrator_email_domains=integrator_email_domains,
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

        self.set_statuses_for_entity(administrative_entity)
        return administrative_entity

    def set_statuses_for_entity(self, administrative_entity):
        for status_value in Submission.STATUS_CHOICES:
            SubmissionWorkflowStatus.objects.get_or_create(
                status=status_value[0], administrative_entity=administrative_entity
            )