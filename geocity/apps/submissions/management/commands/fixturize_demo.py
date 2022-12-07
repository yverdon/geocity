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

from geocity import settings
from geocity.apps.accounts.models import *
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
        with transaction.atomic():
            self.stdout.write("Creating sites...")
            self.setup_sites()
            self.stdout.write("Creating users...")
            self.create_users()
            self.stdout.write("Creating form categories")
            self.create_form_categories()
            self.stdout.write("Creating demo submission...")
            self.create_submission()
            self.stdout.write("Creating template customizations...")
            self.create_template_customization()
            self.stdout.write("Configurating template customizations...")
            self.setup_homepage()
            self.stdout.write("Setting site integrator for selected configurations...")
            self.setup_integrator()
            self.stdout.write("Fixturize succeed!")

    def setup_sites(self):
        Site.objects.get_or_create(domain=settings.DEFAULT_SITE, name="default site")

        # custom sites
        Site.objects.get_or_create(domain="yverdon.localhost", name="yverdon")
        Site.objects.get_or_create(domain="grandson.localhost", name="grandson")
        Site.objects.get_or_create(domain="vevey.localhost", name="vevey")
        Site.objects.get_or_create(domain="lausanne.localhost", name="lausanne")

        # Site for internal use
        # TODO: we shouldn't need this ! Either we need forward the site for internal calls
        # or there should be a default site. For now this should have no impact because
        # the API is not filtered by site.
        # see https://github.com/yverdon/geocity/issues/525
        Site.objects.get_or_create(domain="web", name="web (internal calls)")

    def setup_integrator(self):
        integrator = Group.objects.get(name="integrator")
        SiteProfile.objects.filter(site__name="yverdon").update(integrator=integrator)
        AdministrativeEntity.objects.update(integrator=integrator)
        FormCategory.objects.update(integrator=integrator)
        Form.objects.update(integrator=integrator)
        ContactType.objects.update(integrator=integrator)
        ComplementaryDocumentType.objects.update(integrator=integrator)
        SubmissionAmendField.objects.update(integrator=integrator)

    def create_users(self):

        administrative_entity_yverdon = AdministrativeEntity.objects.create(
            name="Démo Yverdon",
            ofs_id=5938,
            link="https://mapnv.ch",
            archive_link="https://mapnv.ch",
            geom="SRID=2056;MultiPolygon (((2538391 1176432, 2538027 1178201, 2538485 1178804, 2537777 1179199, 2536748 1178450, 2536123 1179647, 2537382 1180593, 2537143 1181623, 2538651 1183257, 2540368 1183236, 2541252 1181093, 2541460 1180458, 2540160 1179543, 2540097 1178877, 2538391 1176432)))",
        )

        administrative_entity_yverdon.tags.add("yverdon")
        administrative_entity_yverdon.sites.add(Site.objects.get(name="yverdon"))
        administrative_entity_yverdon.sites.add(Site.objects.get(name="default site"))

        administrative_entity_grandson = AdministrativeEntity.objects.create(
            name="Démo Grandson",
            ofs_id=5938,
            link="https://mapnv.ch",
            archive_link="https://mapnv.ch",
            geom="SRID=2056;MultiPolygon (((2543281 1184952, 2542053 1186731, 2541148 1186887, 2538214 1186367, 2537195 1184609, 2537153 1183330, 2537757 1182653, 2539317 1182404, 2543281 1184952)))",
        )

        administrative_entity_grandson.tags.add("grandson")
        administrative_entity_grandson.sites.add(Site.objects.get(name="grandson"))
        administrative_entity_grandson.sites.add(Site.objects.get(name="default site"))

        administrative_entity_lausanne = AdministrativeEntity.objects.create(
            name="Démo Lausanne",
            ofs_id=5586,
            link="https://mapnv.ch",
            archive_link="https://mapnv.ch",
            geom="SRID=2056;MultiPolygon (((2533045 1151566, 2533789 1154840, 2538236 1155380, 2541064 1154989, 2541790 1157408, 2540934 1160087, 2543074 1161259, 2546553 1159715, 2545399 1156329, 2542757 1155361, 2542348 1153798, 2542497 1152347, 2540692 1150617, 2535855 1152105, 2533045 1151566)),((2529938 1157110, 2529789 1160329, 2532245 1161557, 2532580 1160273, 2530831 1158934, 2530757 1157259, 2529938 1157110)))",
        )

        administrative_entity_lausanne.tags.add("lausanne")
        administrative_entity_lausanne.sites.add(Site.objects.get(name="lausanne"))
        administrative_entity_lausanne.sites.add(Site.objects.get(name="default site"))

        administrative_entity_vevey = AdministrativeEntity.objects.create(
            name="Démo Vevey",
            ofs_id=5890,
            link="https://mapnv.ch",
            archive_link="https://mapnv.ch",
            geom="SRID=2056;MultiPolygon (((2553381 1146430, 2553679 1145798, 2553660 1145500, 2554777 1145296, 2555502 1145965, 2554870 1146617, 2555335 1147398, 2555037 1147417, 2554311 1146803, 2553418 1146840, 2553269 1146524, 2553381 1146430)))",
        )

        administrative_entity_vevey.tags.add("vevey")
        administrative_entity_vevey.sites.add(Site.objects.get(name="vevey"))
        administrative_entity_vevey.sites.add(Site.objects.get(name="default site"))

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

        UserProfile.objects.create(
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
        UserProfile.objects.create(
            user=user,
            address="Rue du Port",
            zipcode=1234,
            city="Lausanne",
            phone_first="000 00 00 00",
            phone_second="000 00 00 00",
        )
        self.stdout.write("user / demo")

        submission_ct = ContentType.objects.get_for_model(Submission)
        secretariat_permissions = Permission.objects.filter(
            codename__in=[
                "amend_submission",
                "classify_submission",
            ],
            content_type=submission_ct,
        )

        reports_request_ct = ContentType.objects.get_for_model(Report)
        secretariat_permissions_reports = Permission.objects.filter(
            codename__in=[
                "can_generate_pdf",
            ],
            content_type=reports_request_ct,
        )
        # user = self.create_user(
        #     "pilot",
        #     "pilot",
        #     administrative_entity_yverdon,
        #     email="yverdon-squad+pilot@liip.ch",
        # )
        # user.user_permissions.set(
        #     secretariat_permissions.union(secretariat_permissions_reports)
        # )
        # self.stdout.write("pilot / demo")

        # user = self.create_user(
        #     "pilot-2",
        #     "pilot-2",
        #     administrative_entity_grandson,
        #     email="yverdon-squad+pilot-2@liip.ch",
        # )
        # user.user_permissions.set(secretariat_permissions)
        # self.stdout.write("pilot-2 / demo")

        # secretary_groups = Group.objects.filter(name__in=["pilot", "pilot-2"])
        # PermitDepartment.objects.filter(group__in=secretary_groups).update(
        #     is_backoffice=True
        # )

        # user = self.create_user(
        #     "validator",
        #     "validator",
        #     administrative_entity_yverdon,
        #     is_default_validator=True,
        #     email="yverdon-squad+validator@liip.ch",
        # )
        # Group.objects.get(name="validator").permissions.add(
        #     Permission.objects.get(
        #         codename="validate_submission", content_type=submission_ct
        #     )
        # )

        # validator_group = Group.objects.get(name="validator")
        # department = PermitDepartment.objects.get(group=validator_group)
        # department.is_validator = True
        # department.save()

        # self.stdout.write("validator / demo")

        # user = self.create_user(
        #     "validator-2",
        #     "validator-2",
        #     administrative_entity_yverdon,
        #     email="yverdon-squad+validator-2@liip.ch",
        # )
        # Group.objects.get(name="validator-2").permissions.add(
        #     Permission.objects.get(
        #         codename="validate_submission", content_type=submission_ct
        #     )
        # )
        # self.stdout.write("validator-2 / demo")

        # user = self.create_user(
        #     "integrator",
        #     "integrator",
        #     administrative_entity_yverdon,
        #     is_default_validator=True,
        #     is_integrator_admin=True,
        #     is_staff=True,
        #     email="yverdon-squad+integrator@liip.ch",
        # )

        # # set the required permissions for the integrator group
        # Group.objects.get(name="integrator").permissions.set(
        #     get_integrator_permissions()
        # )
        # self.stdout.write("integrator / demo")

        # Insert status choices from Submission and insert status for adminsitrative_entity
        for status_value in Submission.STATUS_CHOICES:
            for entity in [
                administrative_entity_yverdon,
                administrative_entity_grandson,
                administrative_entity_lausanne,
                administrative_entity_vevey,
            ]:
                SubmissionWorkflowStatus.objects.get_or_create(
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
        UserProfile.objects.create(
            user=user,
            address="Rue du Lac",
            zipcode=1400,
            city="Yverdon",
        )
        PermitDepartment.objects.create(
            group=group,
            is_validator=False,
            is_integrator_admin=is_integrator_admin,
            is_backoffice=False,
            administrative_entity=administrative_entity,
            is_default_validator=is_default_validator,
        )

        return user

    def create_form_categories(self):
        fields = {
            "comment": Field.objects.create(
                name="Commentaire",
                input_type="text",
                is_mandatory=False,
            ),
            "width": Field.objects.create(
                name="Largeur [m]",
                input_type="number",
                placeholder="3",
                help_text="Largeur en mètres",
                is_mandatory=False,
            ),
            "title": Field.objects.create(
                name="Texte permettant de séparer visuellement les champs",
                input_type="title",
                help_text="Ce texte permet d'expliquer en détail à l'utilisateur les pourquoi et le comment des informations à fournir",
                is_mandatory=False,
            ),
            "height": Field.objects.create(
                name="Hauteur [m]",
                input_type="number",
                placeholder="2",
                help_text="Longueur en mètres",
                is_mandatory=False,
            ),
            "plan": Field.objects.create(
                name="Plan de situation",
                input_type="file",
                help_text="Plan complémentaire détaillant votre projet",
                is_mandatory=False,
            ),
            "adresse": Field.objects.create(
                name="Adresse",
                input_type="address",
                placeholder="Place Pestalozzi 2, 1400 Yverdon-les-Bains",
                is_mandatory=False,
            ),
            "adresse_geocode": Field.objects.create(
                name="Adresse avec géocodage",
                input_type="address",
                placeholder="Place Pestalozzi 2, 1400 Yverdon-les-Bains",
                is_mandatory=False,
                store_geometry_for_address_field=True,
            ),
            "date": Field.objects.create(
                name="Date",
                input_type="date",
                is_mandatory=False,
            ),
            "checkbox": Field.objects.create(
                name="Impact sur la chaussée",
                input_type="checkbox",
                is_mandatory=False,
            ),
            "list_single": Field.objects.create(
                name="À moins de 3m d'un arbre",
                input_type="list_single",
                is_mandatory=False,
                choices="oui\nnon",
            ),
            "list_multiple": Field.objects.create(
                name="À moins de 3m d'un arbre",
                input_type="list_multiple",
                is_mandatory=False,
                choices="Déviation trafic\nHoraire prolongé\nSon>90dB",
            ),
        }

        # Administrative entities
        administrative_entity_yverdon = AdministrativeEntity.objects.get(
            name="Démo Yverdon",
        )
        administrative_entity_yverdon.tags.add("yverdon")
        administrative_entity_grandson = AdministrativeEntity.objects.get(
            name="Démo Grandson",
        )
        administrative_entity_grandson.tags.add("grandson")
        administrative_entity_lausanne = AdministrativeEntity.objects.get(
            name="Démo Lausanne",
        )
        administrative_entity_lausanne.tags.add("lausanne")
        administrative_entity_vevey = AdministrativeEntity.objects.get(
            name="Démo Vevey",
        )
        administrative_entity_vevey.tags.add("vevey")

        # Forms
        form_categories = [
            (
                "Stationnement (ex. de demande devant être prolongée)",
                [
                    (
                        "Demande de macaron",
                        administrative_entity_yverdon,
                        fields["comment"],
                        fields["date"],
                    ),
                    (
                        "Accès au centre-ville historique",
                        administrative_entity_lausanne,
                        fields["plan"],
                        fields["width"],
                        fields["comment"],
                        fields["title"],
                        fields["date"],
                        fields["checkbox"],
                        fields["adresse"],
                        fields["list_multiple"],
                    ),
                ],
            ),
            (
                "Événements sur la voie publique",
                [
                    (
                        "Événement sportif",
                        administrative_entity_yverdon,
                        fields["plan"],
                        fields["width"],
                        fields["comment"],
                        fields["title"],
                        fields["date"],
                        fields["checkbox"],
                        fields["adresse"],
                        fields["list_multiple"],
                    ),
                    (
                        "Événement culturel",
                        administrative_entity_yverdon,
                        fields["plan"],
                        fields["width"],
                        fields["comment"],
                        fields["title"],
                        fields["date"],
                        fields["checkbox"],
                        fields["adresse"],
                        fields["list_multiple"],
                    ),
                    (
                        "Événement politique",
                        administrative_entity_grandson,
                        fields["plan"],
                        fields["width"],
                        fields["comment"],
                        fields["title"],
                        fields["date"],
                        fields["checkbox"],
                        fields["adresse"],
                        fields["list_multiple"],
                    ),
                    (
                        "Événement commercial",
                        administrative_entity_grandson,
                        fields["plan"],
                        fields["width"],
                        fields["comment"],
                        fields["title"],
                        fields["date"],
                        fields["checkbox"],
                        fields["adresse"],
                        fields["list_multiple"],
                    ),
                ],
            ),
            (
                "Chantier",
                [
                    (
                        "Permis de fouille",
                        administrative_entity_grandson,
                        fields["width"],
                        fields["height"],
                        fields["title"],
                        fields["comment"],
                        fields["adresse"],
                        fields["adresse_geocode"],
                        fields["checkbox"],
                        fields["list_single"],
                    ),
                    (
                        "Permis de dépôt",
                        administrative_entity_vevey,
                        fields["width"],
                        fields["height"],
                        fields["comment"],
                        fields["title"],
                        fields["adresse"],
                        fields["adresse_geocode"],
                        fields["checkbox"],
                    ),
                ],
            ),
            (
                "Subventions (ex. de demande sans géométrie ni période temporelle)",
                [
                    (
                        "Prime éco-mobilité",
                        administrative_entity_vevey,
                        fields["comment"],
                    ),
                    (
                        "Abonnement de bus",
                        administrative_entity_vevey,
                        fields["comment"],
                    ),
                ],
            ),
        ]

        additional_information_text = """
        Texte expliquant la ou les conditions particulière(s) s'appliquant à cette demande.
        Un document pdf peut également être proposé à l'utilisateur, par exemple pour les conditions
        de remise en état après une fouille sur le domaine public
        """

        form_order = 0

        for form_category, objs in form_categories:
            form_category_obj = FormCategory.objects.create(name=form_category)
            form_category_obj.tags.add(unaccent(form_category))
            ContactType.objects.create(
                type=CONTACT_TYPE_OTHER,
                form_category=form_category_obj,
                is_mandatory=False,
            )

            for form, administrative_entity, *fields in objs:
                form_obj = Form.objects.create(
                    name=form,
                    category=form_category_obj,
                    is_public=True,
                    notify_services=True,
                    document_enabled=True,
                    publication_enabled=True,
                    permanent_publication_enabled=True,
                    services_to_notify=f"yverdon-squad+admin@liip.ch",
                    additional_information=additional_information_text,
                    order=form_order,
                )
                form_order += 1
                form_obj.administrative_entities.set([administrative_entity])

                self.create_document_types(form_obj)
                for order, field in enumerate(fields):
                    FormField.objects.create(field=field, form=form_obj, order=order)

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

    def create_submission(self):

        demo_author = User.objects.get(username="user")
        demo_administrative_entity = AdministrativeEntity.objects.get(
            name="Démo Yverdon"
        )
        demo_form = Form.objects.first()
        Form.objects.filter(id=5).update(requires_validation_document=False)
        demo_form_no_validation_document = Form.objects.filter(
            requires_validation_document=False
        ).first()
        department = PermitDepartment.objects.filter(
            administrative_entity=demo_administrative_entity,
            is_validator=True,
        ).first()

        # Basic submission
        submission = Submission.objects.create(
            status=Submission.STATUS_DRAFT,
            administrative_entity=demo_administrative_entity,
            author=demo_author,
        )

        SelectedForm.objects.create(submission=submission, form=demo_form)

        SubmissionGeoTime.objects.create(
            submission=submission,
            starts_at=timezone.now(),
            ends_at=timezone.now(),
            geom="GEOMETRYCOLLECTION(MULTILINESTRING((2539096.09997796 1181119.41274907,2539094.37477054 1181134.07701214,2539094.37477054 1181134.07701214)), MULTIPOLYGON(((2539102.56950579 1181128.03878617,2539101.27560022 1181139.2526344,2539111.19554289 1181140.11523811,2539111.62684475 1181134.07701214,2539111.62684475 1181134.07701214,2539102.56950579 1181128.03878617))), MULTIPOINT((2539076.69139448 1181128.47008802)))",
        )

        # Submission to Classify with no validation document required
        submission2 = Submission.objects.create(
            status=Submission.STATUS_PROCESSING,
            administrative_entity=demo_administrative_entity,
            author=demo_author,
            is_public=True,
        )

        SubmissionValidation.objects.get_or_create(
            submission=submission2,
            department=department,
            validation_status=SubmissionValidation.STATUS_APPROVED,
            comment_before="Ce projet n'est pas admissible, veuillez l'améliorer.",
            comment_during="Les améliorations ont été prise en compte.",
            comment_after="Excellent projet qui bénéficiera à la communauté.",
        )

        SelectedForm.objects.create(
            submission=submission2,
            form=demo_form_no_validation_document,
        )

        SubmissionGeoTime.objects.create(
            submission=submission2,
            starts_at=timezone.now(),
            ends_at=timezone.now(),
            geom="GEOMETRYCOLLECTION(MULTILINESTRING((2539096.09997796 1181119.41274907,2539094.37477054 1181134.07701214,2539094.37477054 1181134.07701214)), MULTIPOLYGON(((2539102.56950579 1181128.03878617,2539101.27560022 1181139.2526344,2539111.19554289 1181140.11523811,2539111.62684475 1181134.07701214,2539111.62684475 1181134.07701214,2539102.56950579 1181128.03878617))), MULTIPOINT((2539076.69139448 1181128.47008802)))",
        )

        # Submission to Classify with mixed objects requiring and not requiring validation document
        submission3 = Submission.objects.create(
            status=Submission.STATUS_PROCESSING,
            administrative_entity=demo_administrative_entity,
            author=demo_author,
            is_public=True,
        )

        SubmissionValidation.objects.get_or_create(
            submission=submission3,
            department=department,
            validation_status=SubmissionValidation.STATUS_APPROVED,
            comment_before="Ce projet n'est pas admissible, veuillez l'améliorer.",
            comment_during="Les améliorations ont été prise en compte.",
            comment_after="Excellent projet qui bénéficiera à la communauté.",
        )

        SelectedForm.objects.create(submission=submission3, form=demo_form)

        SelectedForm.objects.create(
            submission=submission3,
            form=demo_form_no_validation_document,
        )

        SubmissionGeoTime.objects.create(
            submission=submission3,
            starts_at=timezone.now(),
            ends_at=timezone.now(),
            geom="GEOMETRYCOLLECTION(MULTILINESTRING((2539096.09997796 1181119.41274907,2539094.37477054 1181134.07701214,2539094.37477054 1181134.07701214)), MULTIPOLYGON(((2539102.56950579 1181128.03878617,2539101.27560022 1181139.2526344,2539111.19554289 1181140.11523811,2539111.62684475 1181134.07701214,2539111.62684475 1181134.07701214,2539102.56950579 1181128.03878617))), MULTIPOINT((2539076.69139448 1181128.47008802)))",
        )

        # Submission to Classify with validation document required
        submission4 = Submission.objects.create(
            status=Submission.STATUS_PROCESSING,
            administrative_entity=demo_administrative_entity,
            author=demo_author,
            is_public=True,
        )

        SubmissionValidation.objects.get_or_create(
            submission=submission4,
            department=department,
            validation_status=SubmissionValidation.STATUS_APPROVED,
            comment_before="Ce projet n'est pas admissible, veuillez l'améliorer.",
            comment_during="Les améliorations ont été prise en compte.",
            comment_after="Excellent projet qui bénéficiera à la communauté.",
        )
        SelectedForm.objects.create(submission=submission4, form=demo_form)

        SubmissionGeoTime.objects.create(
            submission=submission4,
            starts_at=timezone.now(),
            ends_at=timezone.now(),
            geom="GEOMETRYCOLLECTION(MULTILINESTRING((2539096.09997796 1181119.41274907,2539094.37477054 1181134.07701214,2539094.37477054 1181134.07701214)), MULTIPOLYGON(((2539102.56950579 1181128.03878617,2539101.27560022 1181139.2526344,2539111.19554289 1181140.11523811,2539111.62684475 1181134.07701214,2539111.62684475 1181134.07701214,2539102.56950579 1181128.03878617))), MULTIPOINT((2539076.69139448 1181128.47008802)))",
        )

        submission5 = Submission.objects.create(
            status=Submission.STATUS_PROCESSING,
            administrative_entity=demo_administrative_entity,
            author=demo_author,
            is_public=True,
        )

        SubmissionValidation.objects.get_or_create(
            submission=submission5,
            department=department,
            validation_status=SubmissionValidation.STATUS_APPROVED,
            comment_before="Ce projet n'est pas admissible, veuillez l'améliorer.",
            comment_during="Les améliorations ont été prise en compte.",
            comment_after="Excellent projet qui bénéficiera à la communauté.",
        )

        SelectedForm.objects.create(
            submission=submission5,
            form=Form.objects.last(),
        )

        SubmissionGeoTime.objects.create(
            submission=submission5,
            starts_at=timezone.now(),
            ends_at=timezone.now(),
            geom="GEOMETRYCOLLECTION(MULTILINESTRING((2539096.09997796 1181119.41274907,2539094.37477054 1181134.07701214,2539094.37477054 1181134.07701214)), MULTIPOLYGON(((2539102.56950579 1181128.03878617,2539101.27560022 1181139.2526344,2539111.19554289 1181140.11523811,2539111.62684475 1181134.07701214,2539111.62684475 1181134.07701214,2539102.56950579 1181128.03878617))), MULTIPOINT((2539076.69139448 1181128.47008802)))",
        )

        # Submission with pending validations

        submission6 = Submission.objects.create(
            status=Submission.STATUS_AWAITING_VALIDATION,
            administrative_entity=demo_administrative_entity,
            author=demo_author,
            is_public=True,
        )

        SubmissionValidation.objects.get_or_create(
            submission=submission6,
            department=department,
        )

        SelectedForm.objects.create(
            submission=submission6,
            form=Form.objects.last(),
        )

        SubmissionGeoTime.objects.create(
            submission=submission6,
            starts_at=timezone.now(),
            ends_at=timezone.now(),
            geom="GEOMETRYCOLLECTION(MULTILINESTRING((2539096.09997796 1181119.41274907,2539094.37477054 1181134.07701214,2539094.37477054 1181134.07701214)), MULTIPOLYGON(((2539102.56950579 1181128.03878617,2539101.27560022 1181139.2526344,2539111.19554289 1181140.11523811,2539111.62684475 1181134.07701214,2539111.62684475 1181134.07701214,2539102.56950579 1181128.03878617))), MULTIPOINT((2539076.69139448 1181128.47008802)))",
        )

        # Submission to Classify with mixed objects with lots of text for print demo
        submission7 = Submission.objects.create(
            status=Submission.STATUS_PROCESSING,
            administrative_entity=demo_administrative_entity,
            author=demo_author,
            is_public=True,
        )
        # SubmissionValidations with long text
        SubmissionValidation.objects.get_or_create(
            submission=submission7,
            department=department,
            validation_status=SubmissionValidation.STATUS_APPROVED,
            comment_before=demo_small_text,
            comment_during=demo_small_text,
            comment_after=demo_small_text,
        )
        SubmissionValidation.objects.get_or_create(
            submission=submission7,
            department=PermitDepartment.objects.get(group__name="validator-2"),
            validation_status=SubmissionValidation.STATUS_APPROVED,
            comment_before=demo_small_text,
            comment_during=demo_small_text,
            comment_after=demo_small_text,
        )

        SelectedForm.objects.create(submission=submission7, form=demo_form)

        SelectedForm.objects.create(
            submission=submission7,
            form=demo_form_no_validation_document,
        )

        SubmissionGeoTime.objects.create(
            submission=submission7,
            starts_at=timezone.now(),
            ends_at=timezone.now(),
            geom="GEOMETRYCOLLECTION(MULTIPOLYGON(((2539078 1181121, 2539092 1181084, 2539118 1181111, 2539099 1181105, 2539078 1181121))))",
        )

        # Amend properties with long text
        amend_field_1 = SubmissionAmendField.objects.create(
            name="Commentaire interne",
            is_visible_by_author=False,
        )
        amend_field_1.forms.set([demo_form, demo_form_no_validation_document])
        amend_field_2 = SubmissionAmendField.objects.create(
            name="Commentaire visible par le requérant",
            is_visible_by_author=True,
        )
        amend_field_2.forms.set([demo_form, demo_form_no_validation_document])
        amend_field_3 = SubmissionAmendField.objects.create(
            name="Commentaire interne visible par les validateurs",
            is_visible_by_author=False,
            is_visible_by_validators=True,
        )
        amend_field_3.forms.set([demo_form, demo_form_no_validation_document])
        selected_form_1 = SelectedForm.objects.get(
            submission=submission7,
            form=demo_form,
        )
        selected_form_2 = SelectedForm.objects.get(
            submission=submission7,
            form=demo_form_no_validation_document,
        )
        SubmissionAmendFieldValue.objects.create(
            field=amend_field_1,
            form=selected_form_1,
            value=demo_small_text,
        )
        SubmissionAmendFieldValue.objects.create(
            field=amend_field_1,
            form=selected_form_2,
            value=demo_small_text,
        )
        SubmissionAmendFieldValue.objects.create(
            field=amend_field_2,
            form=selected_form_1,
            value=demo_small_text,
        )
        SubmissionAmendFieldValue.objects.create(
            field=amend_field_2,
            form=selected_form_2,
            value=demo_small_text,
        )
        SubmissionAmendFieldValue.objects.create(
            field=amend_field_3,
            form=selected_form_1,
            value=demo_small_text,
        )
        SubmissionAmendFieldValue.objects.create(
            field=amend_field_3,
            form=selected_form_2,
            value=demo_small_text,
        )

        # Set default values for fields
        for field_obj in Field.objects.all():
            for selected_form in [
                selected_form_1,
                selected_form_2,
            ]:
                if field_obj.input_type == Field.INPUT_TYPE_DATE:
                    FieldValue.objects.create(
                        field=field_obj,
                        selected_form=selected_form,
                        value={"val": "01.01.2021"},
                    )
                if field_obj.input_type == Field.INPUT_TYPE_ADDRESS:
                    FieldValue.objects.create(
                        field=field_obj,
                        selected_form=selected_form,
                        value={"val": "Place pestalozzi 2, 1400 Yverdon-les-Bains"},
                    )
                if field_obj.input_type == Field.INPUT_TYPE_CHECKBOX:
                    FieldValue.objects.create(
                        field=field_obj,
                        selected_form=selected_form,
                        value={"val": True},
                    )
                if field_obj.input_type == Field.INPUT_TYPE_NUMBER:
                    FieldValue.objects.create(
                        field=field_obj,
                        selected_form=selected_form,
                        value={"val": 42},
                    )
                if field_obj.input_type == Field.INPUT_TYPE_LIST_SINGLE:
                    FieldValue.objects.create(
                        field=field_obj,
                        selected_form=selected_form,
                        value={"val": "Oui"},
                    )
                if field_obj.input_type == Field.INPUT_TYPE_LIST_MULTIPLE:
                    FieldValue.objects.create(
                        field=field_obj,
                        selected_form=selected_form,
                        value={"val": "Le bon choix"},
                    )
                if (
                    field_obj.input_type == Field.INPUT_TYPE_TEXT
                    or field_obj.input_type == Field.INPUT_TYPE_REGEX
                    or field_obj.input_type == Field.INPUT_TYPE_TITLE
                ):
                    FieldValue.objects.create(
                        field=field_obj,
                        selected_form=selected_form,
                        value={"val": demo_small_text},
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

    def setup_homepage(self):
        config.APPLICATION_TITLE = "Démo Geocity"
        config.APPLICATION_SUBTITLE = "Simplifiez votre administration"
        config.APPLICATION_DESCRIPTION = """<p>Essayez l'application à l'aide des différents comptes et rôles disponibles (utilisateur / mot de passe):</p>
        <ul>
        <li><strong>Utilisateur standard</strong>: user / demo</li>
        <li><strong>Pilote</strong> (secrétariat): pilot / demo</li>
        <li><strong>Validateur</strong>: validator / demo</li>
        <li><strong>Validateur 2</strong>: validator-2 / demo</li>
        <li><strong>Intégrateur</strong>: integrator / demo</li>
        <li><strong>Administrateur</strong>: admin / demo</li>
		</ul>
        <p>Consultez les emails générés par l'application sur le <a href="https://mailhog.geocity.ch" target="_blank">webmail de démonstration</a>.</p>
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
            name, form, children = document_type
            parent = ComplementaryDocumentType.objects.create(
                name=name, form=form, parent=None
            )

            for child in children:
                ComplementaryDocumentType.objects.create(
                    name=child, form=None, parent=parent
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
