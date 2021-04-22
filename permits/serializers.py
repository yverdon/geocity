from django.contrib.gis.geos import GEOSGeometry
from django.utils.text import slugify
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from . import models


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
    administrative_entity = PermitAdministrativeEntitySerializer(read_only=True)
    meta_types = MetaTypesField(source="works_object_types", read_only=True)
    works_object_types_names = WorksObjectTypesNames(
        source="works_object_types", read_only=True
    )
    creditor_type = serializers.SerializerMethodField()

    def get_creditor_type(self, obj):
        if obj.creditor_type is not None:
            creditor = obj.get_creditor_type_display()
        elif obj.author.user and obj.creditor_type is None:
            creditor = (
                _("Auteur de la demande, ")
                + f"{obj.author.user.first_name} {obj.author.user.last_name}"
            )
        else:
            creditor = ""
        return creditor

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

        props = models.PermitRequestAmendPropertyValue.objects.filter(
            works_object_type_choice__permit_request=value,
        ).values(
            "property__name", "value", "works_object_type_choice__works_object_type_id"
        )

        properties = {}
        for prop in props:
            wot = f'permit_request_amend_property_value_{prop["works_object_type_choice__works_object_type_id"]}'
            properties[wot] = {
                prop_i["property__name"]: prop_i["value"]
                for prop_i in props
                if prop_i["works_object_type_choice__works_object_type_id"]
                == prop["works_object_type_choice__works_object_type_id"]
            }

        return properties


class WorksObjectPropertyValueSerializer(serializers.RelatedField):
    def to_representation(self, value):

        props = models.WorksObjectPropertyValue.objects.filter(
            works_object_type_choice__permit_request=value,
        ).values(
            "property__name",
            "value__val",
            "works_object_type_choice__works_object_type_id",
        )

        properties = {}
        for prop in props:
            wot = f'works_object_property_value_{prop["works_object_type_choice__works_object_type_id"]}'
            properties[wot] = {
                prop_i["property__name"]: prop_i["value__val"]
                for prop_i in props
                if prop_i["works_object_type_choice__works_object_type_id"]
                == prop["works_object_type_choice__works_object_type_id"]
            }

        return properties


class PermitRequestActorSerializer(serializers.Serializer):
    def to_representation(self, value):
        actors = models.PermitRequestActor.objects.filter(
            permit_request=value
        ).select_related("actor")

        rep = {}
        if actors:
            for i, actor in enumerate(actors, 1):
                for field in actor.actor._meta.fields:
                    rep[slugify(f"permit_request_actor_{i}_{field.name}")] = getattr(
                        actor.actor, field.name
                    )
                rep[
                    f"permit_request_actor_{i}_actor_type"
                ] = actor.get_actor_type_display()

        return rep


class PermitRequestGeoTimeSerializer(gis_serializers.GeoFeatureModelSerializer):
    permit_request = PermitRequestSerializer(read_only=True)

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


class PermitRequestGeoTimeSingleGeometrySerializer(
    gis_serializers.GeoFeatureModelSerializer
):
    permit_request_geo_time_start_date = serializers.DateTimeField()
    permit_request_geo_time_end_date = serializers.DateTimeField()
    singlegeom = gis_serializers.GeometrySerializerMethodField()

    def get_start_date(self, obj):
        return (
            obj.permit_request_geo_time_start_date
            if obj.permit_request_geo_time_start_date
            else None
        )

    def get_end_date(self, obj):
        return (
            obj.permit_request_geo_time_end_date
            if obj.permit_request_geo_time_end_date
            else None
        )

    def get_singlegeom(self, obj):
        return GEOSGeometry(obj.singlegeom) if obj.singlegeom else None

    class Meta:
        model = models.PermitRequestGeoTime
        geo_field = "singlegeom"
        fields = (
            "permit_request_geo_time_start_date",
            "permit_request_geo_time_end_date",
        )


class PermitRequestGeoTimeGeoJSONSerializer(serializers.Serializer):
    """
        In order to serialize the object as a GeoJSON a queryset has to be passed,
        however, the queryset could have many geometry types in a single row as well as
        many rows with different geometries, in order to generate a single layer from
        all the possible results, the geometries have to be aggregated.
        The max and min dates are determined as well from a Raw SQL.

        Note: Here we need the geo_time queryset as the source (value), since the
        geometry and the dates will be aggregated, but the comments and external links
        will be retrieved and grouped from it.
    """

    def to_representation(self, value):

        geo_time_qs = value.all()

        if not geo_time_qs:
            return {
                "geometry": {"type": "Point", "coordinates": []},
                "properties": {
                    "permit_request_geo_time_start_date": None,
                    "permit_request_geo_time_end_date": None,
                    "permit_request_geo_time_comments": [],
                    "permit_request_geo_time_external_links": [],
                },
            }

        else:
            raw_qs = models.PermitRequestGeoTime.objects.raw(
                "SELECT pr.permit_request_id as id, "
                "MIN(pr.starts_at) as permit_request_geo_time_start_date, "
                "MAX(pr.ends_at) as permit_request_geo_time_end_date, "
                "ST_SetSRID(ST_extent(pr.geom), 2056) as singlegeom "
                "FROM permits_permitrequestgeotime as pr "
                "WHERE pr.permit_request_id = %s "
                "GROUP BY pr.permit_request_id",
                [geo_time_qs.first().permit_request_id],
            )
            result = [
                PermitRequestGeoTimeSingleGeometrySerializer(
                    annotated_qs, read_only=True
                ).data
                for annotated_qs in raw_qs
            ]

            # The aggregation will return just one row, therefore
            result = result[0]

            # Insert empty geometry if there is none
            if not result["geometry"]:
                result["geometry"] = {"type": "Point", "coordinates": []}

            # Collect the comments and external links from all possible rows
            result["properties"]["permit_request_geo_time_comments"] = [
                obj.comment for obj in geo_time_qs
            ]
            result["properties"]["permit_request_geo_time_external_links"] = [
                obj.external_link for obj in geo_time_qs if obj.external_link
            ]

            return result


class PermitRequestPrintSerializer(gis_serializers.GeoFeatureModelSerializer):
    permit_request = PermitRequestSerializer(source="*", read_only=True)
    works_object_property_value = WorksObjectPropertyValueSerializer(
        source="*", read_only=True
    )
    permit_request_amend_property_value = PermitRequestAmendPropertyValueSerializer(
        source="*", read_only=True
    )
    permit_request_actor = PermitRequestActorSerializer(source="*", read_only=True)
    geo_envelop = PermitRequestGeoTimeGeoJSONSerializer(
        source="geo_time", read_only=True
    )

    class Meta:
        model = models.PermitRequest
        geo_field = "geo_time"
        fields = (
            "permit_request",
            "permit_request_amend_property_value",
            "works_object_property_value",
            "permit_request_actor",
            "geo_envelop",
        )

    def to_representation(self, value):
        rep = super().to_representation(value)

        # Flattening the Geometry
        rep["geometry"] = rep["properties"]["geo_envelop"]["geometry"]
        for field, value in rep["properties"]["geo_envelop"]["properties"].items():
            rep["properties"][field] = value
        del rep["properties"]["geo_envelop"]

        # Flattening the permit_request
        for field, value in rep["properties"]["permit_request"].items():
            rep["properties"][f"permit_request_{field}"] = value
        del rep["properties"]["permit_request"]

        # Flattening the rest of related fields
        related_fields_to_flatten = [
            "permit_request_actor",
            "works_object_property_value",
            "permit_request_amend_property_value",
        ]

        for field_to_flatten in related_fields_to_flatten:
            for field, value in rep["properties"][field_to_flatten].items():
                rep["properties"][field] = value
            del rep["properties"][field_to_flatten]

        return rep
