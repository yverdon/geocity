from django.utils.text import slugify
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from . import models
from .services import (
    get_permit_request_amend_custom_properties,
    get_permit_request_properties,
)


class PermitAdministrativeEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PermitAdministrativeEntity
        fields = ("name",)

    def to_representation(self, value):
        return value.name


class MetaTypesField(serializers.RelatedField):
    def to_representation(self, value):
        meta_types = {wot.works_type.meta_type for wot in value.all()}
        return list(meta_types)


class PermitRequestSerializer(serializers.ModelSerializer):

    administrative_entity = PermitAdministrativeEntitySerializer(
        many=False, read_only=True
    )
    meta_types = MetaTypesField(source="works_object_types", read_only=True)

    class Meta:
        model = models.PermitRequest
        fields = (
            "id",
            "status",
            "administrative_entity",
            "works_object_types",
            "creditor_type",
            "meta_types",
        )


class PermitRequestAmendPropertyValueSerializer(serializers.RelatedField):
    def to_representation(self, value):
        works_object_types = [
            works_object_type
            for works_object_type, prop in get_permit_request_amend_custom_properties(
                value
            )
        ]
        props = models.PermitRequestAmendPropertyValue.objects.filter(
            works_object_type_choice__permit_request=value,
            works_object_type_choice__works_object_type__in=works_object_types,
        ).values("property__name", "value", "works_object_type_choice__works_object_type__id")

        return {
            slugify(
                f"{prop['works_object_type_choice__works_object_type__id']}-{prop['property__name']}"
            ): prop['value']
            for prop in props
        }


class WorksObjectPropertyValueSerializer(serializers.RelatedField):
    def to_representation(self, value):
        works_object_types = [
            works_object_type
            for works_object_type, prop in get_permit_request_properties(value)
        ]

        props = models.WorksObjectPropertyValue.objects.filter(
            works_object_type_choice__permit_request=value,
            works_object_type_choice__works_object_type__in=works_object_types,
        ).values("property__name", "value__val", "works_object_type_choice__works_object_type__id")

        return {
            slugify(
                f"{prop['works_object_type_choice__works_object_type__id']}-{prop['property__name']}"
            ): prop["value__val"]
            for prop in props
        }


class PermitActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PermitActor
        fields = "__all__"


class PermitRequestActorSerializer(serializers.RelatedField):
    def to_representation(self, value):
        actors = models.PermitRequestActor.objects.filter(
            permit_request=value
        ).prefetch_related("actor")

        rep = {}
        for i, actor in enumerate(actors, 1):
            actor_data = PermitActorSerializer(instance=actor.actor).data
            for k, v in actor_data.items():
                rep[slugify(f"{i}-{k}")] = v
        return rep


class PermitRequestGeoTimeSerializer(gis_serializers.GeoFeatureModelSerializer):

    PermitRequest = PermitRequestSerializer(
        source="permit_request", many=False, read_only=True
    )
    WorksObjectPropertyValue = WorksObjectPropertyValueSerializer(
        source="permit_request", many=False, read_only=True
    )
    PermitRequestAmendPropertyValue = PermitRequestAmendPropertyValueSerializer(
        source="permit_request", many=False, read_only=True
    )
    PermitRequestActor = PermitRequestActorSerializer(
        source="permit_request", many=False, read_only=True
    )

    class Meta:
        model = models.PermitRequestGeoTime
        geo_field = "geom"
        fields = (
            "starts_at",
            "ends_at",
            "comment",
            "external_link",
            "PermitRequest",
            "PermitRequestAmendPropertyValue",
            "WorksObjectPropertyValue",
            "PermitRequestActor",
        )

    def to_representation(self, value):
        rep = super().to_representation(value)
        related_fields_to_treat = (
            "PermitRequest",
            "PermitRequestAmendPropertyValue",
            "WorksObjectPropertyValue",
            "PermitRequestActor",
        )

        rep["properties"] = dict(rep["properties"])

        # Flattening + Prefixing
        for field in related_fields_to_treat:
            for k, v in rep["properties"][field].items():
                rep["properties"][f"{field}-{k}"] = v
            del rep["properties"][field]

        # Prefix the properties base fields except the geom (geo_field)
        base_fields = (
            set(self.fields.fields.keys())
            - set(related_fields_to_treat)
            - set(["geom"])
        )
        for field in base_fields:
            rep["properties"][f"PermitRequestGeoTime-{field}"] = rep["properties"][
                field
            ]
            del rep["properties"][field]

        return rep
