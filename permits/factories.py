import factory
import faker

from . import models


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
