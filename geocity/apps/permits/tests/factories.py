from datetime import timezone

import factory
import factory.fuzzy
import faker
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import GeometryCollection, MultiPolygon, Point, Polygon
from django.contrib.sites.models import Site
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Q
from django.utils.text import Truncator

from geocity.apps.accounts import permissions_groups

# Import all models of different apps
from geocity.apps.accounts.models import *
from geocity.apps.forms.models import *
from geocity.apps.reports.models import *
from geocity.apps.submissions.models import *


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    address = factory.Faker("word")
    zipcode = factory.Faker("zipcode")
    city = factory.Faker("city")
    phone_first = Truncator(factory.Faker("phone_number")).chars(19)
    phone_second = Truncator(factory.Faker("phone_number")).chars(19)
    user = factory.SubFactory(
        "geocity.apps.permits.tests.factories.UserFactory", actor=None
    )


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    actor = factory.RelatedFactory(UserProfileFactory, "user")
    password = "password"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = "password"
    is_superuser = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_superuser(*args, **kwargs)


class AdministrativeEntityFactory(factory.django.DjangoModelFactory):
    ofs_id = 0
    name = factory.Faker("company")
    geom = MultiPolygon(Polygon(((1, 1), (1, 2), (2, 2), (1, 1))))

    class Meta:
        model = AdministrativeEntity

    @factory.post_generation
    def workflow_statuses(self, create, extracted, **kwargs):
        if not create:
            return

        extracted = extracted or [v[0] for v in Submission.STATUS_CHOICES]
        for status in extracted:
            SubmissionWorkflowStatus.objects.create(
                status=status,
                administrative_entity=self,
            )

    @factory.post_generation
    def integrator(self, create, extracted, **kwargs):
        if not create:
            return

        self.integrator = extracted

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.tags.add(*extracted)

    @factory.post_generation
    def sites(self, create, extracted, **kwargs):
        if not create or not extracted:
            Site.objects.get_or_create(domain="yverdon.localhost", name="yverdon")
            Site.objects.get_or_create(domain="grandson.localhost", name="grandson")
            Site.objects.get_or_create(domain="vevey.localhost", name="vevey")
            Site.objects.get_or_create(domain="lausanne.localhost", name="lausanne")
            self.sites.set(Site.objects.all())
            return

        self.sites.set(extracted)


class GroupFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Company{}".format(n))

    class Meta:
        model = Group

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            return

        if not extracted:
            submission_ct = ContentType.objects.get_for_model(Submission)
            amend_permission = Permission.objects.get(
                codename="amend_submission", content_type=submission_ct
            )
            extracted = [amend_permission]

        for permission in extracted:
            self.permissions.add(permission)


class PermitDepartmentFactory(factory.django.DjangoModelFactory):
    is_default_validator = False
    is_validator = False
    is_integrator_admin = False
    is_backoffice = False
    administrative_entity = factory.SubFactory(AdministrativeEntityFactory)
    group = factory.SubFactory(GroupFactory)

    class Meta:
        model = PermitDepartment


class IntegratorPermitDepartmentFactory(factory.django.DjangoModelFactory):
    is_default_validator = False
    is_validator = False
    is_integrator_admin = True
    is_backoffice = False
    administrative_entity = factory.SubFactory(AdministrativeEntityFactory)
    group = factory.SubFactory(GroupFactory)

    class Meta:
        model = PermitDepartment


class SecretariatGroupFactory(GroupFactory):
    department = factory.RelatedFactory(PermitDepartmentFactory, "group")

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            return

        if not extracted:
            submission_ct = ContentType.objects.get_for_model(Submission)
            extracted = list(
                Permission.objects.filter(
                    codename__in=["amend_submission", "classify_submission"],
                    content_type=submission_ct,
                )
            )

        for permission in extracted:
            self.permissions.add(permission)


class ValidatorGroupFactory(GroupFactory):
    department = factory.RelatedFactory(PermitDepartmentFactory, "group")

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            return

        if not extracted:
            submission_ct = ContentType.objects.get_for_model(Submission)
            validate_permission = Permission.objects.get(
                codename="validate_submission", content_type=submission_ct
            )
            extracted = [validate_permission]

        for permission in extracted:
            self.permissions.add(permission)


class IntegratorGroupFactory(GroupFactory):
    department = factory.RelatedFactory(IntegratorPermitDepartmentFactory, "group")

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            return

        if not extracted:
            extracted = list(
                Permission.objects.filter(
                    (
                        (
                            Q(content_type__app_label="submissions")
                            & Q(
                                content_type__model__in=permissions_groups.INTEGRATOR_REQUIRED_MODELS_PERMISSIONS
                            )
                        )
                        | (
                            Q(content_type__app_label="reports")
                            & Q(
                                content_type__model__in=permissions_groups.INTEGRATOR_REPORTS_MODELS_PERMISSIONS
                            )
                        )
                    )
                    | Q(codename__in=permissions_groups.OTHER_PERMISSIONS_CODENAMES)
                )
            )

        for permission in extracted:
            self.permissions.add(permission)


class SecretariatUserFactory(UserFactory):
    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if not extracted:
            extracted = [SecretariatGroupFactory()]

        for group in extracted:
            self.groups.add(group)


class ValidatorUserFactory(UserFactory):
    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if not extracted:
            extracted = [ValidatorGroupFactory()]

        for group in extracted:
            self.groups.add(group)


class IntegratorUserFactory(UserFactory):
    is_staff = True

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if not extracted:
            extracted = [IntegratorGroupFactory()]

        for group in extracted:
            self.groups.add(group)


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    address = factory.Faker("street_address")
    zipcode = factory.Faker("zipcode")
    city = factory.Faker("city")
    phone = Truncator(factory.Faker("phone_number")).chars(19)


class FormCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FormCategory

    name = factory.Faker("word")
    tags = "form_category_a"

    @factory.post_generation
    def integrator(self, create, extracted, **kwargs):
        if not create:
            return

        self.integrator = extracted

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.tags.add(*extracted)


class FormFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Form

    name = factory.Faker("word")
    form_category = factory.SubFactory(FormCategoryFactory)
    is_public = True
        
    @factory.post_generation
    def integrator(self, create, extracted, **kwargs):
        if not create:
            return

        self.integrator = extracted
        
    @factory.post_generation
    def administrative_entities(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.administrative_entities.add(*extracted)
        
        
class FormWithoutGeometryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Form

    name = factory.Faker("word")
    form_category = factory.SubFactory(FormCategoryFactory)
    is_public = True
    has_geometry_point = False
    has_geometry_line = False
    has_geometry_polygon = False

    @factory.post_generation
    def integrator(self, create, extracted, **kwargs):
        if not create:
            return

        self.integrator = extracted

    @factory.post_generation
    def administrative_entities(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.administrative_entities.add(*extracted)



class ContactTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactType

    form_category = factory.SubFactory(FormCategoryFactory)

    @factory.post_generation
    def integrator(self, create, extracted, **kwargs):
        if not create:
            return

        self.integrator = extracted


class SubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Submission

    administrative_entity = factory.SubFactory(AdministrativeEntityFactory)
    user_profile = factory.SubFactory(UserProfileFactory)


class FieldFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Field

    name = factory.Faker("word")
    placeholder = factory.Faker("word")
    help_text = factory.Faker("word")
    input_type = Field.INPUT_TYPE_TEXT
    order = factory.Sequence(int)

    @factory.post_generation
    def integrator(self, create, extracted, **kwargs):
        if not create:
            return

        self.integrator = extracted


class FieldFactoryTypeAddress(factory.django.DjangoModelFactory):
    class Meta:
        model = Field

    name = factory.Faker("word")
    input_type = Field.INPUT_TYPE_ADDRESS
    order = factory.Sequence(int)


class FieldFactoryTypeFile(factory.django.DjangoModelFactory):
    class Meta:
        model = Field

    name = factory.Faker("word")
    input_type = Field.INPUT_TYPE_FILE
    order = factory.Sequence(int)


class FieldFactoryTypeTitle(factory.django.DjangoModelFactory):
    class Meta:
        model = Field

    name = factory.Faker("word")
    help_text = factory.Faker("word")
    input_type = Field.INPUT_TYPE_TITLE
    order = factory.Sequence(int)


class FieldFactoryTypeFileDownload(factory.django.DjangoModelFactory):
    class Meta:
        model = Field

    name = factory.Faker("word")
    help_text = factory.Faker("word")
    input_type = Field.INPUT_TYPE_FILE_DOWNLOAD
    order = factory.Sequence(int)
    file_download = SimpleUploadedFile("file.pdf", "contents".encode())


class SelectedFormFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SelectedForm

    submission = factory.SubFactory(SubmissionFactory)
    form = factory.SubFactory(FormFactory)


class FieldValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FieldValue

    value = factory.LazyFunction(lambda: {"val": faker.Faker().word()})
    field = factory.SubFactory(FieldFactory)
    selected_form = factory.SubFactory(SelectedFormFactory)


class SubmissionValidationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubmissionValidation

    department = factory.SubFactory(PermitDepartmentFactory)
    submission = factory.SubFactory(
        SubmissionFactory, status=Submission.STATUS_AWAITING_VALIDATION
    )


class SubmissionGeoTimeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubmissionGeoTime

    submission = factory.SubFactory(SubmissionFactory)
    starts_at = factory.Faker("date_time", tzinfo=timezone.utc)
    ends_at = factory.Faker("date_time", tzinfo=timezone.utc)
    geom = factory.LazyFunction(
        lambda: GeometryCollection(Point(faker.Faker().latlng()))
    )


class SubmissionAmendFieldFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubmissionAmendField

    name = factory.Faker("word")

    @factory.post_generation
    def integrator(self, create, extracted, **kwargs):
        if not create:
            return

        self.integrator = extracted


class SubmissionAmendFieldValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubmissionAmendFieldValue

    field = factory.SubFactory(SubmissionAmendFieldFactory)
    selected_form = factory.SubFactory(SelectedFormFactory)
    value = factory.Faker("word")


class TemplateCustomizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TemplateCustomization

    templatename = "mycustompage"
    application_title = "mycustomtitle"
    application_subtitle = "mycustomsubtitle"
    application_description = "mycustomdescription"


class ComplementaryDocumentTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ComplementaryDocumentType

    name = factory.Faker("name")


class ParentComplementaryDocumentTypeFactory(ComplementaryDocumentTypeFactory):
    forms = factory.SubFactory(FormFactory)
    parent = None
    integrator = None


class ChildComplementaryDocumentTypeFactory(ComplementaryDocumentTypeFactory):
    forms = None
    parent = factory.SubFactory(ParentComplementaryDocumentTypeFactory)


class ComplementaryDocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubmissionComplementaryDocument

    document = factory.django.FileField(filename="awesome_file.pdf")
    description = factory.Faker("sentence")
    # the "PermitRequestComplementaryDocument.STATUS_CANCELED" status
    # has extra logic, so to avoid any weird issues, it isn't among the choices
    status = factory.fuzzy.FuzzyChoice(
        choices=[
            SubmissionComplementaryDocument.STATUS_OTHER,
            SubmissionComplementaryDocument.STATUS_TEMP,
            SubmissionComplementaryDocument.STATUS_CANCELED,
        ]
    )
    owner = factory.SubFactory(UserFactory)
    submission = factory.SubFactory(SubmissionFactory)
    document_type = factory.SubFactory(ChildComplementaryDocumentTypeFactory)
    is_public = False

    @factory.post_generation
    def authorised_departments(self, create, extracted, **kwargs):
        if not create:
            return

        self.authorised_departments.add(*extracted)


class SubmissionInquiryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubmissionInquiry

    submitter = factory.SubFactory(UserFactory)
    submission = factory.SubFactory(SubmissionFactory)
    start_date = factory.Faker("date")
    end_date = factory.Faker("date")


class ArchivedPermitRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArchivedSubmission

    submission = factory.SubFactory(SubmissionFactory)
    archivist = factory.SubFactory(UserFactory)
