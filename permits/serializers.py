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


class WorksObjectTypesNames(serializers.RelatedField):
    def to_representation(self, value):
        wot_names = {wot.id: str(wot) for wot in value.all()}
        return wot_names


class PermitRequestSerializer(serializers.ModelSerializer):
    administrative_entity = PermitAdministrativeEntitySerializer(
        many=False, read_only=True
    )
    meta_types = MetaTypesField(source="works_object_types", read_only=True)
    works_object_types_names = WorksObjectTypesNames(
        source="works_object_types", read_only=True
    )

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
            "works_object_types_names",
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
        ).values(
            "property__name", "value", "works_object_type_choice__works_object_type__id"
        )

        properties = {}
        for prop in props:
            if (
                prop["works_object_type_choice__works_object_type__id"]
                not in properties.keys()
            ):
                properties[prop["works_object_type_choice__works_object_type__id"]] = {
                    prop["property__name"]: prop["value"]
                }
            else:
                properties[
                    prop["works_object_type_choice__works_object_type__id"]
                ].update({prop["property__name"]: prop["value"]})

        return properties


class WorksObjectPropertyValueSerializer(serializers.RelatedField):
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

        properties = {}
        for prop in props:
            if (
                prop["works_object_type_choice__works_object_type__id"]
                not in properties.keys()
            ):
                properties[prop["works_object_type_choice__works_object_type__id"]] = {
                    prop["property__name"]: prop["value__val"]
                }
            else:
                properties[
                    prop["works_object_type_choice__works_object_type__id"]
                ].update({prop["property__name"]: prop["value__val"]})

        return properties


class PermitRequestActorSerializer(serializers.Serializer):
    def to_representation(self, value):
        actors = models.PermitRequestActor.objects.filter(
            permit_request=value
        ).prefetch_related("actor")

        rep = {}
        for i, actor in enumerate(actors, 1):
            actor_fields = [field.name for field in actor.actor._meta.fields]
            for field in actor_fields:
                rep[slugify(f"{i}-{field}")] = getattr(actor.actor, field)
            rep[f"{i}-actor-type"] = models.ACTOR_TYPE_CHOICES[actor.actor_type][1]
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
            "PermitRequestAmendPropertyValue",
            "WorksObjectPropertyValue",
            "PermitRequestActor",
            "Geo",
        )

    def to_representation(self, value):
        geotime_fields_to_process = [
            "starts_at",
            "ends_at",
            "comment",
            "external_link",
        ]

        related_fields_to_process = [
            field_name
            for field_name in self.fields.keys()
            if field_name not in {"Geo", "geo_time"}
        ]

        rep = super().to_representation(value)
        rep = dict(rep)

        # Early opt-out if no Date ni Geom
        if not rep["geometry"]:

            PermitRequest = PermitRequestSerializer(
                value, many=False, read_only=True
            ).data
            for k, v in PermitRequest.items():
                rep["properties"][f"PermitRequest-{k}"] = v

            rep["geometry"] = {"type": "Point", "coordinates": []}
            for field in geotime_fields_to_process:
                rep["properties"][f"PermitRequestGeoTime-{field}"] = None

        else:
            for geo_entry, value in enumerate(rep["properties"]["Geo"]):
                for k, v in rep["properties"]["Geo"][geo_entry]["properties"][
                    "permit_request"
                ].items():
                    rep["properties"][f"PermitRequest-{k}"] = v

                if not rep["properties"]["Geo"][geo_entry]["geometry"]:
                    rep["geometry"] = {"type": "Point", "coordinates": []}
                else:
                    rep["geometry"] = rep["properties"]["Geo"][geo_entry]["geometry"]

                try:
                    for field in geotime_fields_to_process:
                        rep["properties"][f"PermitRequestGeoTime-{field}"] = rep[
                            "properties"
                        ]["Geo"][geo_entry]["properties"][field]
                except KeyError:
                    for field in geotime_fields_to_process:
                        rep["properties"][f"PermitRequestGeoTime-{field}"] = None

        # Flattening + Prefixing
        for field in related_fields_to_process:
            for k, v in rep["properties"][field].items():
                rep["properties"][f"{field}-{k}"] = v
            del rep["properties"][field]
        # Some Human Readable values
        creditor_type = rep["properties"]["PermitRequest-creditor_type"]
        rep["properties"]["PermitRequest-creditor_type"] = (
            models.ACTOR_TYPE_CHOICES[creditor_type]
            if creditor_type is not None
            else models.ACTOR_TYPE_CHOICES[0][1]
        )

        del rep["properties"]["Geo"]

        return rep
