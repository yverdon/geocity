import factory
import faker
from gpf.models import Actor, AdministrativeEntity

from . import models


class GpfActorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Actor

    firstname = factory.Faker('first_name')
    name = factory.Faker('last_name')
    email = factory.Faker('email')


class PermitRequestActorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PermitActor

    firstname = factory.Faker('first_name')
    name = factory.Faker('last_name')
    email = factory.Faker('email')


class AdministrativeEntityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdministrativeEntity

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

    administrative_entity = factory.SubFactory(AdministrativeEntityFactory)
    author = factory.SubFactory(GpfActorFactory)


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
