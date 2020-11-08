from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.text import Truncator

import factory
import faker

from . import models


class PermitAuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PermitAuthor

    address = factory.Faker('word')
    zipcode = factory.Faker('zipcode')
    city = factory.Faker('city')
    phone_first = Truncator(factory.Faker('phone_number')).chars(19)
    phone_second = Truncator(factory.Faker('phone_number')).chars(19)


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


class PermitAdministrativeEntityFactory(factory.django.DjangoModelFactory):
    ofs_id = 0
    name = factory.Faker('company')

    class Meta:
        model = models.PermitAdministrativeEntity

    @factory.post_generation
    def workflow_statuses(self, create, extracted, **kwargs):
        if not create:
            return

        extracted = extracted or [v[0] for v in models.PermitRequest.STATUS_CHOICES]
        for status in extracted:
            models.PermitWorkflowStatus.objects.create(status=status, administrative_entity=self)


class PermitDepartmentFactory(factory.django.DjangoModelFactory):
    is_default_validator = False
    is_validator = False
    is_admin = False
    is_archeologist = False
    administrative_entity = factory.SubFactory(PermitAdministrativeEntityFactory)
    group = factory.SubFactory("permits.factories.GroupFactory")

    class Meta:
        model = models.PermitDepartment


class GroupFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("company")

    class Meta:
        model = Group

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            return

        if not extracted:
            permit_request_ct = ContentType.objects.get_for_model(models.PermitRequest)
            amend_permission = Permission.objects.get(codename="amend_permit_request", content_type=permit_request_ct)
            extracted = [amend_permission]

        for permission in extracted:
            self.permissions.add(permission)


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
                    codename__in=[
                        "amend_permit_request",
                        "classify_permit_request",
                        "modify_permit_request",
                    ],
                    content_type=permit_request_ct
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
                codename="validate_permit_request",
                content_type=permit_request_ct
            )
            extracted = [validate_permission]

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


class PermitRequestActorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PermitActor

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')


class WorksObjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorksObject

    name = factory.Faker('word')


class WorksTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorksType

    name = factory.Faker('word')


class PermitRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PermitRequest

    administrative_entity = factory.SubFactory(PermitAdministrativeEntityFactory)
    author = factory.SubFactory(PermitAuthorFactory)


class WorksObjectPropertyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorksObjectProperty

    name = factory.Faker('word')
    input_type = models.WorksObjectProperty.INPUT_TYPE_TEXT


class WorksObjectTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorksObjectType

    works_object = factory.SubFactory(WorksObjectFactory)
    works_type = factory.SubFactory(WorksTypeFactory)


class WorksObjectTypeChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorksObjectTypeChoice

    permit_request = factory.SubFactory(PermitRequestFactory)
    works_object_type = factory.SubFactory(WorksObjectTypeFactory)


class WorksObjectPropertyValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorksObjectPropertyValue

    value = factory.LazyFunction(lambda: {'val': faker.Faker().word()})
    property = factory.SubFactory(WorksObjectPropertyFactory)
    works_object_type_choice = factory.SubFactory(WorksObjectTypeChoiceFactory)


class PermitRequestValidationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PermitRequestValidation

    department = factory.SubFactory(PermitDepartmentFactory)
    permit_request = factory.SubFactory(PermitRequestFactory, status=models.PermitRequest.STATUS_AWAITING_VALIDATION)
