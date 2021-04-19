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
            "intersected_geometries",
            "meta_types",
        )


class PermitRequestAmendPropertyValueSerializer(serializers.Serializer):
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
        ).values(
            "property__name", "value", "works_object_type_choice__works_object_type__id"
        )

        return {
            slugify(
                f"{prop['works_object_type_choice__works_object_type__id']}-{prop['property__name']}"
            ): prop["value"]
            for prop in props
        }


class WorksObjectPropertyValueSerializer(serializers.Serializer):
    def to_representation(self, value):
        works_object_types = [
            works_object_type
            for works_object_type, prop in get_permit_request_properties(value)
        ]

        props = models.WorksObjectPropertyValue.objects.filter(
            works_object_type_choice__permit_request=value,
            works_object_type_choice__works_object_type__in=works_object_types,
        ).values(
            "property__name",
            "value__val",
            "works_object_type_choice__works_object_type__id",
        )

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


class PermitRequestActorSerializer(serializers.Serializer):
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
    permit_request = PermitRequestSerializer(many=False, read_only=True)

    class Meta:
        model = models.PermitRequestGeoTime
        geo_field = "geom"
        fields = (
            "permit_request",
            "starts_at",
            "ends_at",
            "comment",
            "external_link",
        )


class PermitRequestGeoTimeGeoJSONSerializer(serializers.Serializer):
    def to_representation(self, value):

        geotime_qs = models.PermitRequestGeoTime.objects.filter(
            permit_request_id=value.id
        )

        result = [
            serialized_geotime.data
            for serialized_geotime in [
                PermitRequestGeoTimeSerializer(geotime, many=False, read_only=True)
                for geotime in geotime_qs
            ]
        ]
        return result


class PermitRequestPrintSerializer(gis_serializers.GeoFeatureModelSerializer):
    PermitRequest = PermitRequestSerializer(source="*", many=False, read_only=True)
    WorksObjectPropertyValue = WorksObjectPropertyValueSerializer(
        source="*", many=False, read_only=True
    )
    PermitRequestAmendPropertyValue = PermitRequestAmendPropertyValueSerializer(
        source="*", many=False, read_only=True
    )
    PermitRequestActor = PermitRequestActorSerializer(
        source="*", many=False, read_only=True
    )
    Geo = PermitRequestGeoTimeGeoJSONSerializer(source="*", many=False, read_only=True)

    class Meta:
        model = models.PermitRequest
        geo_field = "geo_time"
        fields = (
            "PermitRequest",
            "PermitRequestAmendPropertyValue",
            "WorksObjectPropertyValue",
            "PermitRequestActor",
            "Geo",
        )

    def to_representation(self, value):
        geotime_fields_to_process = (
            "starts_at",
            "ends_at",
            "comment",
            "external_link",
        )

        related_fields_to_process = set(self.fields.fields.keys()) - {"Geo", "geo_time"}

        rep = super().to_representation(value)
        rep = dict(rep)
        # # DELETE ME AFTER USE
        # import ipdb; ipdb.set_trace()
        # # ###################

        if not rep["geometry"]:
            rep["geometry"] = {"type": "Point", "coordinates": []}
            for field in geotime_fields_to_process:
                rep["properties"][f"PermitRequestGeoTime-{field}"] = None
        else:
            if not rep["properties"]["Geo"][0]["geometry"]:
                rep["geometry"] = {"type": "Point", "coordinates": []}
            else:
                rep["geometry"] = rep["properties"]["Geo"][0]["geometry"]
            try:
                for field in geotime_fields_to_process:
                    rep["properties"][f"PermitRequestGeoTime-{field}"] = rep[
                        "properties"
                    ]["Geo"][0]["properties"][field]
            except KeyError:
                for field in geotime_fields_to_process:
                    rep["properties"][f"PermitRequestGeoTime-{field}"] = None

        # Flattening + Prefixing
        rep["properties"] = dict(rep["properties"])
        for field in related_fields_to_process:
            for k, v in rep["properties"][field].items():
                rep["properties"][f"{field}-{k}"] = v
            del rep["properties"][field]

        del rep["properties"]["Geo"]

        return rep
