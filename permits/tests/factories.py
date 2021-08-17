from datetime import timezone

import factory
import faker
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import GeometryCollection, Point
from django.utils.text import Truncator
from permits import models, admin
from django.db.models import Q
from taggit.managers import TaggableManager


class PermitAuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PermitAuthor

    address = factory.Faker("word")
    zipcode = factory.Faker("zipcode")
    city = factory.Faker("city")
    phone_first = Truncator(factory.Faker("phone_number")).chars(19)
    phone_second = Truncator(factory.Faker("phone_number")).chars(19)
    user = factory.SubFactory("permits.tests.factories.UserFactory", actor=None)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    actor = factory.RelatedFactory(PermitAuthorFactory, "user")
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


class PermitAdministrativeEntityFactory(factory.django.DjangoModelFactory):
    ofs_id = 0
    name = factory.Faker("company")

    class Meta:
        model = models.PermitAdministrativeEntity

    @factory.post_generation
    def workflow_statuses(self, create, extracted, **kwargs):
        if not create:
            return

        extracted = extracted or [v[0] for v in models.PermitRequest.STATUS_CHOICES]
        for status in extracted:
            models.PermitWorkflowStatus.objects.create(
                status=status, administrative_entity=self,
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

        self.tags.set(*extracted)


class GroupFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Company{}".format(n))

    class Meta:
        model = Group

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            return

        if not extracted:
            permit_request_ct = ContentType.objects.get_for_model(models.PermitRequest)
            amend_permission = Permission.objects.get(
                codename="amend_permit_request", content_type=permit_request_ct
            )
            extracted = [amend_permission]

        for permission in extracted:
            self.permissions.add(permission)


class PermitDepartmentFactory(factory.django.DjangoModelFactory):
    is_default_validator = False
    is_validator = False
    is_integrator_admin = False
    is_archeologist = False
    administrative_entity = factory.SubFactory(PermitAdministrativeEntityFactory)
    group = factory.SubFactory(GroupFactory)

    class Meta:
        model = models.PermitDepartment


class IntegratorPermitDepartmentFactory(factory.django.DjangoModelFactory):
    is_default_validator = False
    is_validator = False
    is_integrator_admin = True
    is_archeologist = False
    administrative_entity = factory.SubFactory(PermitAdministrativeEntityFactory)
    group = factory.SubFactory(GroupFactory)

    class Meta:
        model = models.PermitDepartment


class SecretariatGroupFactory(GroupFactory):
    department = factory.RelatedFactory(PermitDepartmentFactory, "group")

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            return

        if not extracted:
            permit_request_ct = ContentType.objects.get_for_model(models.PermitRequest)
            extracted = list(
                Permission.objects.filter(
                    codename__in=["amend_permit_request", "classify_permit_request"],
                    content_type=permit_request_ct,
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
            permit_request_ct = ContentType.objects.get_for_model(models.PermitRequest)
            validate_permission = Permission.objects.get(
                codename="validate_permit_request", content_type=permit_request_ct
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
                        Q(content_type__app_label="permits")
                        & Q(
                            content_type__model__in=admin.INTEGRATOR_PERMITS_MODELS_PERMISSIONS
                        )
                    )
                    | Q(codename__in=admin.OTHER_PERMISSIONS_CODENAMES)
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


class PermitActorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PermitActor

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    address = factory.Faker("street_address")
    zipcode = factory.Faker("zipcode")
    city = factory.Faker("city")
    phone = Truncator(factory.Faker("phone_number")).chars(19)


class WorksObjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorksObject

    name = factory.Faker("word")

    @factory.post_generation
    def integrator(self, create, extracted, **kwargs):
        if not create:
            return

        self.integrator = extracted


class WorksTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorksType

    name = factory.Faker("word")
    tags = "work_type_a"

    @factory.post_generation
    def integrator(self, create, extracted, **kwargs):
        if not create:
            return

        self.integrator = extracted

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.tags.set(*extracted)


class PermitActorTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PermitActorType

    works_type = factory.SubFactory(WorksTypeFactory)

    @factory.post_generation
    def integrator(self, create, extracted, **kwargs):
        if not create:
            return

        self.integrator = extracted


class PermitRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PermitRequest

    administrative_entity = factory.SubFactory(PermitAdministrativeEntityFactory)
    author = factory.SubFactory(PermitAuthorFactory)


class WorksObjectPropertyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorksObjectProperty

    name = factory.Faker("word")
    placeholder = factory.Faker("word")
    help_text = factory.Faker("word")
    input_type = models.WorksObjectProperty.INPUT_TYPE_TEXT
    order = factory.Sequence(int)

    @factory.post_generation
    def integrator(self, create, extracted, **kwargs):
        if not create:
            return

        self.integrator = extracted


class WorksObjectPropertyFactoryTypeAddress(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorksObjectProperty

    name = factory.Faker("word")
    input_type = models.WorksObjectProperty.INPUT_TYPE_ADDRESS
    order = factory.Sequence(int)


class WorksObjectPropertyFactoryTypeFile(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorksObjectProperty

    name = factory.Faker("word")
    input_type = models.WorksObjectProperty.INPUT_TYPE_FILE
    order = factory.Sequence(int)


class WorksObjectTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorksObjectType

    works_object = factory.SubFactory(WorksObjectFactory)
    works_type = factory.SubFactory(WorksTypeFactory)
    is_public = True

    @factory.post_generation
    def integrator(self, create, extracted, **kwargs):
        if not create:
            return

        self.integrator = extracted


class WorksObjectTypeWithoutGeometryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorksObjectType

    works_object = factory.SubFactory(WorksObjectFactory)
    works_type = factory.SubFactory(WorksTypeFactory)
    is_public = True
    has_geometry_point = False
    has_geometry_line = False
    has_geometry_polygon = False


class WorksObjectTypeChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorksObjectTypeChoice

    permit_request = factory.SubFactory(PermitRequestFactory)
    works_object_type = factory.SubFactory(WorksObjectTypeFactory)


class WorksObjectPropertyValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorksObjectPropertyValue

    value = factory.LazyFunction(lambda: {"val": faker.Faker().word()})
    property = factory.SubFactory(WorksObjectPropertyFactory)
    works_object_type_choice = factory.SubFactory(WorksObjectTypeChoiceFactory)


class PermitRequestValidationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PermitRequestValidation

    department = factory.SubFactory(PermitDepartmentFactory)
    permit_request = factory.SubFactory(
        PermitRequestFactory, status=models.PermitRequest.STATUS_AWAITING_VALIDATION
    )


class PermitRequestGeoTimeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PermitRequestGeoTime

    permit_request = factory.SubFactory(PermitRequestFactory)
    starts_at = factory.Faker("date_time", tzinfo=timezone.utc)
    ends_at = factory.Faker("date_time", tzinfo=timezone.utc)
    geom = factory.LazyFunction(
        lambda: GeometryCollection(Point(faker.Faker().latlng()))
    )


class PermitRequestAmendPropertyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PermitRequestAmendProperty

    name = factory.Faker("word")

    @factory.post_generation
    def integrator(self, create, extracted, **kwargs):
        if not create:
            return

        self.integrator = extracted


class PermitRequestAmendPropertyValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PermitRequestAmendPropertyValue

    property = factory.SubFactory(PermitRequestAmendPropertyFactory)
    works_object_type_choice = factory.SubFactory(WorksObjectTypeChoiceFactory)
    value = factory.Faker("word")


class QgisProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.QgisProject

    works_object_type = factory.SubFactory(WorksObjectTypeFactory)
    qgis_print_template_name = "atlas"
    qgis_layers = "base,vpoly"


class TemplateCustomizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TemplateCustomization

    templatename = "mycustompage"
    application_title = "mycustomtitle"
    application_subtitle = "mycustomsubtitle"
    application_description = "mycustomdescription"
