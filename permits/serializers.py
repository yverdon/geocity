import json

from collections import OrderedDict
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import AsGeoJSON, Centroid
from django.db.models import Max, Min
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from . import geoservices, models


class PermitAdministrativeEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PermitAdministrativeEntity
        fields = (
            "name",
            "ofs_id",
            "link",
            "phone",
        )


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


class PermitRequestSerializer(serializers.ModelSerializer):
    administrative_entity = PermitAdministrativeEntitySerializer(read_only=True)
    meta_types = MetaTypesField(source="works_object_types", read_only=True)
    works_object_types_names = WorksObjectTypesNames(
        source="works_object_types", read_only=True
    )
    intersected_geometries = serializers.SerializerMethodField()

    def get_intersected_geometries(self, obj):
        return obj.intersected_geometries if obj.intersected_geometries else ""

    class Meta:
        model = models.PermitRequest
        fields = (
            "id",
            "status",
            "shortname",
            "administrative_entity",
            "works_object_types",
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
            "works_object_type__works_object__name",
            "works_object_type__works_type__name",
        )
        amend_props = obj.values(
            "amend_properties__property__name",
            "amend_properties__value",
            "works_object_type_id",
            "works_object_type__works_object__name",
            "works_object_type__works_type__name",
        )
        wot_properties = {}
        amend_properties = {}

        if wot_props:
            for prop in wot_props:
                wot = f'{prop["works_object_type__works_object__name"]} ({prop["works_object_type__works_type__name"]})'
                wot_properties[wot] = {
                    prop_i["properties__property__name"]: prop_i[
                        "properties__value__val"
                    ]
                    for prop_i in wot_props
                    if prop_i["works_object_type_id"] == prop["works_object_type_id"]
                    and prop_i["properties__property__name"]
                }

        for prop in amend_props:
            amends = f'{prop["works_object_type__works_object__name"]} ({prop["works_object_type__works_type__name"]})'
            amend_properties[amends] = {
                prop_i["amend_properties__property__name"]: prop_i[
                    "amend_properties__value"
                ]
                for prop_i in amend_props
                if prop_i["works_object_type_id"] == prop["works_object_type_id"]
                and prop_i["amend_properties__property__name"]
            }

        wot_and_amend_properties = {
            "request_properties": wot_properties,
            "amend_properties": amend_properties,
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
                actor_object = {}
                actor_object["actor_type_display"] = actor.get_actor_type_display()
                for field in actor.actor._meta.fields:
                    actor_object[field.name] = getattr(actor.actor, field.name)
                rep[f"{actor.get_actor_type_display()}"] = actor_object

        return rep


class PermitAuthorSerializer(serializers.ModelSerializer):

    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = models.PermitAuthor
        fields = (
            "first_name",
            "last_name",
            "address",
            "zipcode",
            "city",
            "company_name",
            "vat_number",
            "phone_first",
            "phone_second",
            "email",
        )


class PermitRequestValidationSerializer(serializers.Serializer):
    def to_representation(self, value):
        validations = models.PermitRequestValidation.objects.filter(
            permit_request=value
        )

        rep = {}
        if validations:
            for i, validation in enumerate(validations, 1):
                values = {}
                for field in validation._meta.fields:
                    values[
                        "validation_status"
                    ] = validation.get_validation_status_display()
                    if field.name in [
                        "comment_before",
                        "comment_during",
                        "comment_after",
                    ]:
                        values[field.name] = getattr(validation, field.name)

                rep[validation.department.description] = values
            return rep


class PermitRequestGeoTimeSerializer(gis_serializers.GeoFeatureModelSerializer):
    permit_request = PermitRequestSerializer(read_only=True)

    class Meta:
        model = models.PermitRequestGeoTime
        geo_field = "geom"
        auto_bbox = True
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

    Note: The extract_geom paramter specifies the aggregation function used to represent
    the geometries. If not specified, it will return a boudning box. If specified, it
    will return a multigeometry of the given type (1 for point, 2 for lines, 3 for polys).
    """

    EXTRACT_POINTS = 1
    EXTRACT_LINES = 2
    EXTRACT_POLYS = 3

    def __init__(self, *args, extract_geom=None, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.extract_geom = extract_geom

    def to_representation(self, value):
        geo_time_qs = value.all()
        if not geo_time_qs:
            return {
                "geometry": {"type": "Polygon", "coordinates": []},
                "properties": {
                    "geotime_aggregated": {
                        "start_date": "",
                        "end_date": "",
                        "comments": [],
                        "external_links": [],
                    }
                },
            }

        else:

            if self.extract_geom == self.EXTRACT_POINTS:
                geom_function = geoservices.ExtractPoints("geom")
            elif self.extract_geom == self.EXTRACT_LINES:
                geom_function = geoservices.ExtractLines("geom")
            elif self.extract_geom == self.EXTRACT_POLYS:
                geom_function = geoservices.ExtractPolys("geom")
            else:
                geom_function = geoservices.JoinGeometries("geom")

            aggregated_geotime_qs = geo_time_qs.values("permit_request_id").aggregate(
                permit_request_geo_time_end_date=Max("ends_at"),
                permit_request_geo_time_start_date=Min("starts_at"),
                singlegeom=geom_function,
            )

            result = {"properties": {}}
            if not aggregated_geotime_qs["singlegeom"]:
                result["geometry"] = None
            else:
                result["geometry"] = json.loads(
                    GEOSGeometry(aggregated_geotime_qs["singlegeom"]).json
                )

            geotime_aggregated = {}
            geotime_aggregated["start_date"] = (
                aggregated_geotime_qs["permit_request_geo_time_start_date"].strftime(
                    "%d.%m.%Y %H:%M"
                )
                if aggregated_geotime_qs["permit_request_geo_time_start_date"]
                else ""
            )
            geotime_aggregated["end_date"] = (
                aggregated_geotime_qs["permit_request_geo_time_end_date"].strftime(
                    "%d.%m.%Y %H:%M"
                )
                if aggregated_geotime_qs["permit_request_geo_time_end_date"]
                else ""
            )

            # Collect the comments and external links from all possible rows
            geotime_aggregated["comments"] = [
                obj.comment for obj in geo_time_qs if obj.comment
            ]
            if geotime_aggregated["comments"] == []:
                geotime_aggregated["comments"] = ""

            geotime_aggregated["external_links"] = [
                obj.external_link for obj in geo_time_qs if obj.external_link
            ]

            if geotime_aggregated["external_links"] == []:
                geotime_aggregated["external_links"] = ""

            result["properties"]["geotime_aggregated"] = geotime_aggregated
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
        source="geo_time", read_only=True,
    )

    creditor_type = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    author = PermitAuthorSerializer(read_only=True)
    validations = PermitRequestValidationSerializer(source="*", read_only=True)

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

    def get_status_display(self, obj):
        if obj.status is not None:
            status = obj.get_status_display()
        else:
            status = ""
        return status

    class Meta:
        model = models.PermitRequest
        geo_field = "geo_time"
        id_field = "id"
        fields = (
            "id",
            "permit_request",
            "additional_decision_information",
            "wot_and_amend_properties",
            "permit_request_actor",
            "creditor_type",
            "status_display",
            "author",
            "geo_envelop",
            "validations",
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

        # If the WOT has no geometry, we add the centroid of the administrative entity as a square (polygon)
        if rep["properties"]["geo_envelop"]["geometry"]["coordinates"] == []:
            administrative_entity_name = rep["properties"]["permit_request"][
                "administrative_entity"
            ]["name"]
            administrative_entity = (
                models.PermitAdministrativeEntity.objects.filter(
                    name=administrative_entity_name
                )
                .annotate(centroid_geom=geoservices.JoinGeometries("geom"))
                .first()
            )
            rep["properties"]["geo_envelop"]["geometry"] = json.loads(
                administrative_entity.centroid_geom.geojson
            )

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
        related_fields_to_flatten = ["wot_and_amend_properties"]

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
