from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from . import models, metatypes


class WorksMetaTypeSerializer(serializers.Serializer):
    id =serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    label = serializers.CharField(max_length=200)
    color = serializers.ListField()


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
        fields = ("status", "administrative_entity", "works_object_types", "meta_types")


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

