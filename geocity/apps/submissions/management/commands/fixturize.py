import re
import shutil
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

from geocity import settings
from geocity.apps.accounts.models import *
from geocity.apps.accounts.users import get_integrator_permissions
from geocity.apps.forms.models import *
from geocity.apps.reports.models import *
from geocity.apps.submissions.models import *

# import fixturize file
from ..fixturize_data.generic_example import *


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


def setup_media(images_folder):
    if images_folder:
        image_dir = os.path.join(
            settings.PRIVATE_MEDIA_ROOT, f"permit_requests_uploads/0/"
        )

        if os.path.exists(image_dir):
            shutil.rmtree(image_dir)

        source_dir = (
            "geocity/apps/submissions/management/fixturize_data/images/posters/"
        )
        shutil.copytree(source_dir, image_dir)


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Resetting database...")
        reset_db()
        # setup_media(images_folder)
        self.stdout.write("")
        self.stdout.write("░██████╗███████╗███████╗██████╗░")
        self.stdout.write("██╔════╝██╔════╝██╔════╝██╔══██╗")
        self.stdout.write("╚█████╗░█████╗░░█████╗░░██║░░██║")
        self.stdout.write("░╚═══██╗██╔══╝░░██╔══╝░░██║░░██║")
        self.stdout.write("██████╔╝███████╗███████╗██████╔╝")
        self.stdout.write("╚═════╝░╚══════╝╚══════╝╚═════╝░")
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
                self.stdout.write(" • Creating submissions...")
                self.setup_submission(
                    entity,
                    iterations.get("user_iterations"),
                    administrative_entity,
                    small_text,
                )
                self.stdout.write(" • Creating default report...")
                Report.create_default_report(administrative_entity.id)
            self.stdout.write("Creating template customizations...")
            self.create_template_customization()
            self.stdout.write("Setup template customizations...")
            self.setup_homepage(entities, iterations)
            self.stdout.write("Fixturize succeed ✔")

    def setup_necessary_default_site(self):
        Site.objects.get_or_create(domain=settings.DEFAULT_SITE, name="default site")

    def setup_site(self, entity):
        domain = f"{entity}.localhost"
        Site.objects.get_or_create(domain=domain, name=entity)

    def create_users(self, iterations, entity, domain, administrative_entity):
        """For each administrative entity, create :
        - Administrative entity
        - 1 super user
        - {integrator_iterations} integrators
        - {pilot_iterations} pilots
            - With permissions
            - With group
        - {validator_iterations} validators
        - {user_iterations} users
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
            # Used to manage specific cases on forms
            if (
                form_category.startswith("RENEWAL_REMINDER")
                or form_category.startswith("NO_GEOM_NOR_TIME")
                or form_category.startswith("ADVANCED_MAP_PLUGIN")
                or form_category.startswith("AGENDA")
            ):
                # Remove first word
                form_category_name = form_category.split(" ", 1)[1]
            else:
                form_category_name = form_category

            form_category_obj = self.create_form_category(
                form_category_name, integrator_group
            )
            self.create_contact_form(form_category_obj, integrator_group)

            for form, *fields in objs:
                form_obj, form_order = self.create_form(
                    form,
                    form_category,
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

    def create_form_category(self, form_category, integrator_group):
        form_category_obj = FormCategory.objects.create(
            name=form_category,
            integrator=integrator_group,
        )
        form_category_obj.tags.add(unaccent(form_category))
        return form_category_obj

    def create_contact_form(self, form_category_obj, integrator_group):
        contact_type_other, created = ContactType.objects.get_or_create(name="Autres")
        ContactForm.objects.create(
            type=contact_type_other,
            form_category=form_category_obj,
            is_mandatory=False,
            integrator=integrator_group,
        )

    def create_form(
        self,
        form,
        form_category,
        form_category_obj,
        form_additional_information,
        form_order,
        administrative_entity,
        integrator_group,
    ):
        result = self.setup_form_specific_cases(form_category)

        form_obj = Form.objects.create(
            name=form,
            api_name=convert_string_to_api_key(form),
            category=form_category_obj,
            is_public=True,
            notify_services=True,
            document_enabled=True,
            publication_enabled=True,
            permanent_publication_enabled=True,
            services_to_notify="",
            additional_information=form_additional_information,
            order=form_order,
            integrator=integrator_group,
            has_geometry_point=result.get("has_geometry_point"),
            has_geometry_line=result.get("has_geometry_line"),
            has_geometry_polygon=result.get("has_geometry_polygon"),
            needs_date=result.get("needs_date"),
            start_delay=result.get("start_delay"),
            permit_duration=result.get("permit_duration"),
            expiration_reminder=result.get("expiration_reminder"),
            days_before_reminder=result.get("days_before_reminder"),
            map_widget_configuration=result.get("map_widget_configuration"),
            geo_widget_option=result.get("geo_widget_option"),
            agenda_visible=result.get("agenda_visible"),
        )
        form_obj.administrative_entities.add(administrative_entity)
        form_order += 1

        return form_obj, form_order

    def setup_form_specific_cases(self, form_category):
        has_geometry_point = True
        has_geometry_line = True
        has_geometry_polygon = True
        needs_date = True
        start_delay = None
        permit_duration = None
        expiration_reminder = False
        days_before_reminder = None
        map_widget_configuration = None
        agenda_visible = False
        geo_widget_option = Form.GEO_WIDGET_GENERIC

        # Configure specific form in order to illustrate full potential of Geocity
        # Check if form has RENEWAL_REMINDER or NO_GEOM_NOR_TIME
        if form_category.startswith("RENEWAL_REMINDER"):
            has_geometry_point = True
            has_geometry_line = False
            has_geometry_polygon = False
            needs_date = True
            start_delay = 1
            permit_duration = 2
            expiration_reminder = True
            days_before_reminder = 5
        elif form_category.startswith("NO_GEOM_NOR_TIME"):
            has_geometry_point = False
            has_geometry_line = False
            has_geometry_polygon = False
            needs_date = False
        elif form_category.startswith("ADVANCED_MAP_PLUGIN"):
            map_widget_configuration, _ = MapWidgetConfiguration.objects.get_or_create(
                name="Sélection d'objets",
                configuration=advanced_map_config,
            )
            geo_widget_option = Form.GEO_WIDGET_ADVANCED
        elif form_category.startswith("AGENDA"):
            agenda_visible = True
        result = {
            "has_geometry_point": has_geometry_point,
            "has_geometry_line": has_geometry_line,
            "has_geometry_polygon": has_geometry_polygon,
            "needs_date": needs_date,
            "start_delay": start_delay,
            "permit_duration": permit_duration,
            "expiration_reminder": expiration_reminder,
            "days_before_reminder": days_before_reminder,
            "map_widget_configuration": map_widget_configuration,
            "geo_widget_option": geo_widget_option,
            "agenda_visible": agenda_visible,
        }
        return result

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
        public_if_submission_public = field.get("public_if_submission_public", False)
        api_light = field.get("api_light", False)
        filter_for_api = field.get("filter_for_api", False)
        field, created = Field.objects.get_or_create(
            integrator=integrator,
            name=name,
            api_name=convert_string_to_api_key(name),
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
            public_if_submission_public=public_if_submission_public,
            api_light=api_light,
            filter_for_api=filter_for_api,
        )
        return field

    def create_form_field(self, field, form_obj, order):
        FormField.objects.get_or_create(field=field, form=form_obj, order=order)

    def setup_submission(self, entity, user_iterations, administrative_entity, text):
        forms = administrative_entity.forms
        first_form = forms.first()
        form_no_validation_document = forms.order_by("id")[0]
        form_no_validation_document.requires_validation_document = False
        form_no_validation_document.save()
        last_form = forms.last()
        department = administrative_entity.departments.filter(is_validator=True).first()
        another_department = PermitDepartment.objects.get(
            group__name=f"{entity}-validator"
        )
        comment = """Avant : Ce projet n'est pas admissible, veuillez l'améliorer.
Pendant : Les améliorations ont été prise en compte.
Après : Excellent projet qui bénéficiera à la communauté."""

        sent_date = timezone.now()

        for user_iteration in range(user_iterations):
            username = f"{entity}-user-{user_iteration}"
            user = User.objects.get(username=username)

            # Basic submission
            status = Submission.STATUS_DRAFT
            submission = self.create_submission(status, administrative_entity, user)
            self.create_selected_form(submission, first_form)

            # Submission to Classify with no validation document required
            status = Submission.STATUS_PROCESSING
            submission = self.create_submission(
                status, administrative_entity, user, is_public=True, sent_date=sent_date
            )
            self.create_selected_form(submission, form_no_validation_document)
            validation_status = SubmissionValidation.STATUS_APPROVED
            self.create_submission_validation(
                submission,
                department,
                validation_status,
                comment,
            )

            # Submission to Classify with mixed objects requiring and not requiring validation document
            status = Submission.STATUS_PROCESSING
            submission = self.create_submission(
                status, administrative_entity, user, is_public=True, sent_date=sent_date
            )
            self.create_selected_form(submission, first_form)
            self.create_selected_form(submission, form_no_validation_document)
            validation_status = SubmissionValidation.STATUS_APPROVED
            self.create_submission_validation(
                submission,
                department,
                validation_status,
                comment,
            )

            # Submission to Classify with validation document required
            status = Submission.STATUS_PROCESSING
            submission = self.create_submission(
                status, administrative_entity, user, is_public=True, sent_date=sent_date
            )
            self.create_selected_form(submission, first_form)
            validation_status = SubmissionValidation.STATUS_APPROVED
            self.create_submission_validation(
                submission,
                department,
                validation_status,
                comment,
            )

            # Submission to Classify with validation document required (with another Form)
            status = Submission.STATUS_PROCESSING
            submission = self.create_submission(
                status, administrative_entity, user, is_public=True, sent_date=sent_date
            )
            self.create_selected_form(submission, last_form)
            validation_status = SubmissionValidation.STATUS_APPROVED
            self.create_submission_validation(
                submission,
                department,
                validation_status,
                comment,
            )

            # Submission with pending validations
            status = Submission.STATUS_AWAITING_VALIDATION
            submission = self.create_submission(
                status, administrative_entity, user, is_public=True, sent_date=sent_date
            )
            self.create_selected_form(submission, last_form)
            self.create_submission_validation(submission, department)

            # Submission to Classify with mixed objects with lots of text for print demo
            status = Submission.STATUS_PROCESSING
            submission = self.create_submission(
                status, administrative_entity, user, is_public=True, sent_date=sent_date
            )
            selected_form_1 = self.create_selected_form(submission, first_form)
            selected_form_2 = self.create_selected_form(
                submission, form_no_validation_document
            )
            validation_status = SubmissionValidation.STATUS_APPROVED
            self.create_submission_validation(
                submission,
                department,
                validation_status,
                text,
            )
            self.create_submission_validation(
                submission,
                another_department,
                validation_status,
                text,
            )

            # Amend properties
            name = "Commentaire interne"
            placeholder = "Exemple de texte à saisir"
            help_text = "Explication relative au texte à saisir"
            regex_pattern = ""
            amend_field = self.create_submission_amend_field(
                name,
                placeholder,
                help_text,
                regex_pattern,
                first_form,
                form_no_validation_document,
                is_visible_by_author=False,
            )
            self.create_submission_amend_field_value(amend_field, selected_form_1, text)
            self.create_submission_amend_field_value(amend_field, selected_form_2, text)

            name = "Commentaire visible par le requérant"
            amend_field = self.create_submission_amend_field(
                name,
                placeholder,
                help_text,
                regex_pattern,
                first_form,
                form_no_validation_document,
                is_visible_by_author=True,
            )
            amend_field_with_regex = self.create_submission_amend_field(
                name,
                "CHF 100.-",
                "Saisir une valeur au format suivant CHF 100.-",
                ".*(CHF \d+).*",
                first_form,
                form_no_validation_document,
                is_visible_by_author=True,
            )
            self.create_submission_amend_field_value(amend_field, selected_form_1, text)
            self.create_submission_amend_field_value(
                amend_field_with_regex, selected_form_2, "CHF 100.-"
            )

            name = "Commentaire interne visible par les validateurs"
            amend_field = self.create_submission_amend_field(
                name,
                placeholder,
                help_text,
                regex_pattern,
                first_form,
                form_no_validation_document,
                is_visible_by_author=False,
                is_visible_by_validators=True,
            )
            self.create_submission_amend_field_value(amend_field, selected_form_1, text)
            self.create_submission_amend_field_value(amend_field, selected_form_2, text)

            # Set default values for fields
            self.set_default_values_for_field(
                selected_form_1, selected_form_2, text, user_iteration
            )

    def create_template_customization(self):
        TemplateCustomization.objects.create(
            templatename="geocity",
            application_title="Geocity",
            application_subtitle="Demandes en lignes concenrnant le territoire communal",
            application_description="Demandes en ligne concernant le <b>domaine public</b>",
        )

        TemplateCustomization.objects.create(
            templatename="city",
            application_title="City Admin",
            application_subtitle="Demandes en lignes",
            application_description="Demandes concernant l' <i>administration</i>",
        )

    def setup_homepage(self, entities, iterations):
        application_description_css = """
        <style>
            .login_container {
                width: 100vw;
                position: relative;
                display: flex;
                left: calc(-18vw + 50%);
                background-color:rgba(255,255,255,0.7);
            }

            table {
                border-collapse: separate;
                border-spacing: 0 15px;
            }

            th, td {
                width: 150px;
                text-align: center;
                padding: 5px;
            }

            .btn {
                font-size: smaller;
            }
        </style>
        """

        application_description_js = """
            <script>
                function login(user, role, entity) {
                    number = "";

                    if (role && entity) {
                        element = 'select_' + role + '_' + entity;
                        number = document.getElementById(element).value;
                    }

                    document.getElementById("id_email_or_username").value = user + number;
                    document.getElementById("id_password").value = "demo";
                    document.getElementById("login_button").click();
                }
            </script>
        """

        entity_description = ""
        login_accounts = ""
        for domain, entity in entities.items():
            entity_description += f"<li><b>{entity}</b></li>"

            select_integrator = f"<select id='select_integrator_{entity}'>"
            for integrator_iteration in range(iterations.get("integrator_iterations")):
                select_integrator += f"<option value='{integrator_iteration}'>{integrator_iteration}</option>"

            select_pilot = f"<select id='select_pilot_{entity}'>"
            for pilot_iteration in range(iterations.get("pilot_iterations")):
                select_pilot += (
                    f"<option value='{pilot_iteration}'>{pilot_iteration}</option>"
                )

            select_validator = f"<select id='select_validator_{entity}'>"
            for validator_iteration in range(iterations.get("validator_iterations")):
                select_validator += f"<option value='{validator_iteration}'>{validator_iteration}</option>"

            select_user = f"<select id='select_user_{entity}'>"
            for user_iteration in range(iterations.get("user_iterations")):
                select_user += (
                    f"<option value='{user_iteration}'>{user_iteration}</option>"
                )

            login_accounts += f"<tr><td>{entity}</td>"
            login_accounts += f"<td><button type='button' class='btn btn-info' onclick=\"login('{entity}-superuser', null, null)\">superuser</button></td>"
            login_accounts += f"<td><button type='button' class='btn btn-info' onclick=\"login('{entity}-integrator-', 'integrator', '{entity}').value\">integrator</button>{select_integrator}</td>"
            login_accounts += f"<td><button type='button' class='btn btn-info' onclick=\"login('{entity}-pilot-', 'pilot', '{entity}')\">pilot</button>{select_pilot}</td>"
            login_accounts += f"<td><button type='button' class='btn btn-info' onclick=\"login('{entity}-validator-', 'validator', '{entity}')\">validator</button>{select_validator}</td>"
            login_accounts += f"<td><button type='button' class='btn btn-info' onclick=\"login('{entity}-user-', 'user', '{entity}')\">user</button>{select_user}</td></tr>"

        login_example = f"""
        <ul>
            <li><strong>Administrateur</strong>: {list(entities.values())[0]}-superuser / demo</li>
            <li><strong>Intégrateur</strong>: {list(entities.values())[0]}-integrator-2 / demo</li>
            <li><strong>Pilote</strong> (secrétariat): {list(entities.values())[0]}-pilot-3 / demo</li>
            <li><strong>Validateur</strong>: {list(entities.values())[0]}-validator-3 / demo</li>
            <li><strong>Utilisateur standard</strong>: {list(entities.values())[0]}-user-0 / demo</li>
        </ul>
        """

        automatic_login = f"""
        <div class="automatic_login">
        <h1>Connexion automatique</h1>
        <p>Cliquer sur un bouton pour se connecter. La liste déroulante permet de se connecter sur un autre utilisateur du même rôle</p>
        <table>
            <tr>
                <th>Entité/Rôle</th>
                <th>Administrateur</th>
                <th>Intégrateur</th>
                <th>Pilote</th>
                <th>Validateur</th>
                <th>Utilisateur standard</th>
            </tr>
            {login_accounts}
        </table>
        </div>
        """

        config.APPLICATION_TITLE = "Démo Geocity"
        config.APPLICATION_SUBTITLE = "Simplifiez votre administration"
        config.APPLICATION_DESCRIPTION = f"""
        {application_description_css}
        <p>Essayez l'application à l'aide des différents comptes et rôles disponibles (utilisateur / mot de passe):</p>
        <p>Construction d'un utilisateur : <strong>entité-role-nombre</strong></p>
        <p>Mot de passe par défaut <strong>demo</strong></p>
        <p></p>
        <p>Quelques exemples :</p>
        {login_example}
        <div class="login_container">
            {automatic_login}
        </div>
        {application_description_js}
        """

    # /////////////////////////////////////
    # User superuser
    # /////////////////////////////////////

    def setup_user_superuser(self, entity, domain):
        # Define username
        username = f"{entity}-superuser"

        # Define email
        email = f"{entity}+superuser@{domain}"

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
        email = f"{entity}+integrator-{integrator_iteration}@{domain}"

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
        email = f"{entity}+pilot-{pilot_iteration}@{domain}"

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
            group,
            administrative_entity,
            is_backoffice=True,
            integrator=integrator_group,
        )

        # Set permissions
        permissions = self.get_pilot_permissions()
        group.permissions.set(permissions)

    def get_pilot_permissions(self):
        secretariat_permissions = Permission.objects.filter(
            codename__in=[
                "amend_submission",
                "edit_submission_validations",
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
        email = f"{entity}+validator-{validator_iteration}@{domain}"

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
        email = f"{entity}+user-{user_iteration}@{domain}"

        # Create user
        user = self.create_user(username, email)

        # Create user profile
        self.create_user_profile(user, entity)

    # /////////////////////////////////////
    # Generic functions related to user creation
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
            phone_first="012 345 67 89",
            phone_second="012 345 67 89",
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
        name = f"{entity}"
        administrative_entity = AdministrativeEntity.objects.create(
            name=name,
            ofs_id=ofs_id,
            link="https://mapnv.ch",
            archive_link="https://mapnv.ch",
            geom=geom,
            is_single_form_submissions=True,
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

    # /////////////////////////////////////
    # Submissions
    # /////////////////////////////////////

    def create_submission(
        self, status, administrative_entity, user, is_public=False, sent_date=None
    ):
        submission = Submission.objects.create(
            status=status,
            administrative_entity=administrative_entity,
            author=user,
            is_public=is_public,
            sent_date=sent_date,
        )

        SubmissionGeoTime.objects.create(
            submission=submission,
            starts_at=timezone.now(),
            ends_at=timezone.now(),
            geom="GEOMETRYCOLLECTION(MULTILINESTRING((2539096.09997796 1181119.41274907,2539094.37477054 1181134.07701214,2539094.37477054 1181134.07701214)), MULTIPOLYGON(((2539102.56950579 1181128.03878617,2539101.27560022 1181139.2526344,2539111.19554289 1181140.11523811,2539111.62684475 1181134.07701214,2539111.62684475 1181134.07701214,2539102.56950579 1181128.03878617))), MULTIPOINT((2539076.69139448 1181128.47008802)))",
        )
        return submission

    def create_selected_form(self, submission, form):
        selected_form, created = SelectedForm.objects.get_or_create(
            submission=submission, form=form
        )
        return selected_form

    def create_submission_validation(
        self,
        submission,
        department,
        validation_status=SubmissionValidation.STATUS_REQUESTED,
        comment="",
    ):
        SubmissionValidation.objects.get_or_create(
            submission=submission,
            department=department,
            validation_status=validation_status,
            comment=comment,
        )

    def create_submission_amend_field(
        self,
        name,
        placeholder,
        help_text,
        regex_pattern,
        first_form,
        second_form,
        is_visible_by_author=True,
        is_visible_by_validators=False,
    ):
        amend_field, created = SubmissionAmendField.objects.get_or_create(
            name=name,
            api_name=convert_string_to_api_key(name),
            placeholder=placeholder,
            help_text=help_text,
            regex_pattern=regex_pattern,
            is_visible_by_author=is_visible_by_author,
            is_visible_by_validators=is_visible_by_validators,
        )

        amend_field.forms.set([first_form, second_form])
        return amend_field

    def create_submission_amend_field_value(self, amend_field, selected_form, text):
        SubmissionAmendFieldValue.objects.get_or_create(
            field=amend_field,
            form=selected_form,
            value=text,
        )

    def set_default_values_for_field(
        self, selected_form_1, selected_form_2, text, user_iteration
    ):
        for field_obj in Field.objects.all():
            for selected_form in [
                selected_form_1,
                selected_form_2,
            ]:
                if field_obj.input_type == Field.INPUT_TYPE_DATE:
                    FieldValue.objects.get_or_create(
                        field=field_obj,
                        selected_form=selected_form,
                        value={"val": "01.01.2021"},
                    )
                if field_obj.input_type == Field.INPUT_TYPE_ADDRESS:
                    FieldValue.objects.get_or_create(
                        field=field_obj,
                        selected_form=selected_form,
                        value={"val": "Place pestalozzi 2, 1400 Yverdon-les-Bains"},
                    )
                if field_obj.input_type == Field.INPUT_TYPE_CHECKBOX:
                    FieldValue.objects.get_or_create(
                        field=field_obj,
                        selected_form=selected_form,
                        value={"val": True},
                    )
                if field_obj.input_type == Field.INPUT_TYPE_NUMBER:
                    FieldValue.objects.get_or_create(
                        field=field_obj,
                        selected_form=selected_form,
                        value={"val": 42},
                    )
                if (
                    field_obj.input_type == Field.INPUT_TYPE_LIST_SINGLE
                    or field_obj.input_type == Field.INPUT_TYPE_LIST_MULTIPLE
                ):
                    FieldValue.objects.get_or_create(
                        field=field_obj,
                        selected_form=selected_form,
                        value={"val": field_obj.choices.strip().splitlines()[0]},
                    )
                if (
                    field_obj.input_type == Field.INPUT_TYPE_TEXT
                    or field_obj.input_type == Field.INPUT_TYPE_REGEX
                    or field_obj.input_type == Field.DISPLAY_TITLE
                    or field_obj.input_type == Field.DISPLAY_TEXT
                ):
                    FieldValue.objects.get_or_create(
                        field=field_obj,
                        selected_form=selected_form,
                        value={"val": text},
                    )
                if field_obj.input_type == Field.INPUT_TYPE_FILE:
                    source_dir = "geocity/apps/submissions/management/fixturize_data/images/posters/"
                    num_images = len(os.listdir(source_dir))
                    image_path = (
                        f"permit_requests_uploads/0/{user_iteration%num_images}.jpg"
                    )

                    FieldValue.objects.get_or_create(
                        field=field_obj,
                        selected_form=selected_form,
                        value={"val": image_path},
                    )
