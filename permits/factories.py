from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

import factory
import faker

from . import models


class PermitActorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PermitAuthor

    firstname = factory.Faker('first_name')
    name = factory.Faker('last_name')
    email = factory.Faker('email')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("user_name")
    actor = factory.RelatedFactory(PermitActorFactory, "user")
    password = "password"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class PermitAdministrativeEntityFactory(factory.django.DjangoModelFactory):
    ofs_id = 0
    name = factory.Faker("company")

    class Meta:
        model = models.PermitAdministrativeEntity


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
                    codename__in=["amend_permit_request", "classify_permit_request"], content_type=permit_request_ct
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
            validate_permission = Permission.objects.get(codename="validate_permit_request", content_type=permit_request_ct)
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

    firstname = factory.Faker('first_name')
    name = factory.Faker('last_name')
    email = factory.Faker('email')


class PermitAdministrativeEntityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PermitAdministrativeEntity

    ofs_id = 0
    name = factory.Faker('company')


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
    author = factory.SubFactory(PermitActorFactory)


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
