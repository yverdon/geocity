import json

from collections import OrderedDict
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Max, Min
from django.utils.text import slugify
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from . import geoservices, models


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
        wot_names = {
            wot.id: f"{wot.works_object.name} ({wot.works_type.name})"
            for wot in value.all()
        }
        return wot_names


class PermitUrlSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='permit_request_detail',
    )

    class Meta:
        model = models.PermitRequest
        fields = ['url']


class PermitRequestSerializer(serializers.ModelSerializer):
    administrative_entity = PermitAdministrativeEntitySerializer(read_only=True)
    permit_url = PermitUrlSerializer(read_only=True)
    meta_types = MetaTypesField(source="works_object_types", read_only=True)
    works_object_types_names = WorksObjectTypesNames(
        source="works_object_types", read_only=True
    )
    creditor_type = serializers.SerializerMethodField()
    intersected_geometries = serializers.SerializerMethodField()

    def get_creditor_type(self, obj):
        if obj.creditor_type is not None:
            creditor = obj.get_creditor_type_display()
        elif obj.author:
            if obj.author.user and obj.creditor_type is None:
                creditor = (
                    _("Auteur de la demande, ")
                    + f"{obj.author.user.first_name} {obj.author.user.last_name}"
                )
        else:
            creditor = ""
        return creditor

    def get_intersected_geometries(self, obj):
        return obj.intersected_geometries if obj.intersected_geometries else ""

    class Meta:
        model = models.PermitRequest
        fields = (
            "id",
            "permit_url",
            "status",
            "administrative_entity",
            "works_object_types",
            "creditor_type",
            "meta_types",
            "intersected_geometries",
            "works_object_types_names",
        )


class PropertiesValuesSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = value.all()
        wot_props = obj.values(
            "properties__property__name",
            "properties__value__val",
            "works_object_type_id",
        )
        amend_props = obj.values(
            "amend_properties__property__name",
            "amend_properties__value",
            "works_object_type_id",
        )
        wot_and_amend_properties = {}
        if wot_props:
            for prop in wot_props:
                wot = f'permit_request_works_object_property_value_{prop["works_object_type_id"]}'
                wot_and_amend_properties[wot] = {
                    prop_i["properties__property__name"]: prop_i[
                        "properties__value__val"
                    ]
                    for prop_i in wot_props
                    if prop_i["works_object_type_id"] == prop["works_object_type_id"]
                    and prop_i["properties__property__name"]
                }

        for prop in amend_props:
            amends = (
                f'permit_request_amend_property_value_{prop["works_object_type_id"]}'
            )
            wot_and_amend_properties[amends] = {
                prop_i["amend_properties__property__name"]: prop_i[
                    "amend_properties__value"
                ]
                for prop_i in amend_props
                if prop_i["works_object_type_id"] == prop["works_object_type_id"]
                and prop_i["amend_properties__property__name"]
            }

        return wot_and_amend_properties


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


class PermitRequestGeoTimeGeoJSONSerializer(serializers.Serializer):
    """
    In order to serialize the object as a GeoJSON a queryset has to be passed,
    however, the queryset could have many geometry types in a single row as well as
    many rows with different geometries, in order to generate a single layer from
    all the possible results, the geometries have to be aggregated.

    Note: Here we need the geo_time queryset as the source (value), since the
    geometry and the dates will be aggregated, but the comments
    and external links will be retrieved and grouped from it.
    """

    def to_representation(self, value):

        geo_time_qs = value.all()

        if not geo_time_qs:
            return {
                "geometry": {"type": "Point", "coordinates": []},
                "properties": {
                    "permit_request_geo_time_start_date": "",
                    "permit_request_geo_time_end_date": "",
                    "permit_request_geo_time_comments": [],
                    "permit_request_geo_time_external_links": [],
                },
            }

        else:
            aggregated_geotime_qs = geo_time_qs.values("permit_request_id").aggregate(
                permit_request_geo_time_end_date=Max("ends_at"),
                permit_request_geo_time_start_date=Min("starts_at"),
                singlegeom=geoservices.JoinGeometries("geom"),
            )

            result = {"properties": {}}
            if not aggregated_geotime_qs["singlegeom"]:
                # Insert empty geometry if there is none
                result["geometry"] = {"type": "Point", "coordinates": []}
            else:
                result["geometry"] = json.loads(
                    GEOSGeometry(aggregated_geotime_qs["singlegeom"]).json
                )

            result["properties"]["permit_request_geo_time_start_date"] = (
                aggregated_geotime_qs["permit_request_geo_time_end_date"]
                if aggregated_geotime_qs["permit_request_geo_time_start_date"]
                else ""
            )
            result["properties"]["permit_request_geo_time_end_date"] = (
                aggregated_geotime_qs["permit_request_geo_time_end_date"]
                if aggregated_geotime_qs["permit_request_geo_time_end_date"]
                else ""
            )

            # Collect the comments and external links from all possible rows
            result["properties"]["permit_request_geo_time_comments"] = [
                obj.comment for obj in geo_time_qs if obj.comment
            ]
            result["properties"]["permit_request_geo_time_external_links"] = [
                obj.external_link for obj in geo_time_qs if obj.external_link
            ]
            return result


# Override of real ListSerialier from django-rest-framework-gis
# If you want to add a new structure with dynamic values, just add it to OrderedDict and give him a new function like "super().prefix_to_representation(data)"
# Then in PermitRequestPrintSerializer write this class like the existant "to_representation"
class PermitRequestPrintListSerialier(gis_serializers.ListSerializer):
    @property
    def data(self):
        return super(gis_serializers.ListSerializer, self).data

    def to_representation(self, data):
        """
        Add GeoJSON compatible formatting to a serialized queryset list
        """
        return OrderedDict(
            (
                ("type", "FeatureCollection"),
                (
                    "crs",
                    {
                        "type": "name",
                        "properties": {"name": "urn:ogc:def:crs:EPSG::2056"},
                    },
                ),
                ("features", super().to_representation(data)),
            )
        )


class PermitRequestPrintSerializer(gis_serializers.GeoFeatureModelSerializer):
    permit_request = PermitRequestSerializer(source="*", read_only=True)
    wot_and_amend_properties = PropertiesValuesSerializer(
        source="worksobjecttypechoice_set", read_only=True
    )
    permit_request_actor = PermitRequestActorSerializer(source="*", read_only=True)
    geo_envelop = PermitRequestGeoTimeGeoJSONSerializer(
        source="geo_time", read_only=True
    )

    class Meta:
        model = models.PermitRequest
        geo_field = "geo_time"
        id_field = "id"
        fields = (
            "id",
            "permit_request",
            "wot_and_amend_properties",
            "permit_request_actor",
            "geo_envelop",
        )

    @classmethod
    def many_init(cls, *args, **kwargs):
        super().many_init(cls, *args, **kwargs)

        child_serializer = cls(*args, **kwargs)
        list_kwargs = {"child": child_serializer}
        list_kwargs.update(
            {
                key: value
                for key, value in kwargs.items()
                if key in gis_serializers.LIST_SERIALIZER_KWARGS
            }
        )
        meta = getattr(cls, "Meta", None)
        list_serializer_class = getattr(
            meta, "list_serializer_class", PermitRequestPrintListSerialier
        )
        return list_serializer_class(*args, **list_kwargs)

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
        related_fields_to_flatten = ["permit_request_actor", "wot_and_amend_properties"]

        for field_to_flatten in related_fields_to_flatten:
            for field, value in rep["properties"][field_to_flatten].items():
                rep["properties"][field] = value
            del rep["properties"][field_to_flatten]

        return rep


class PermitRequestFiltersSerializer(serializers.Serializer):
    works_object_type = serializers.IntegerField(default=None, allow_null=True)
    status = serializers.ChoiceField(
        models.PermitRequest.STATUS_CHOICES, default=None, allow_null=True
    )
    geom_type = serializers.ChoiceField(
        ("lines", "points", "polygons"), default=None, allow_null=True
    )
    permit_request_id = serializers.IntegerField(default=None, allow_null=True)
