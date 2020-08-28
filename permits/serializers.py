from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from . import models


class PermitAdministrativeEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PermitAdministrativeEntity
        fields = ('name', )


class PermitRequestSerializer(serializers.ModelSerializer):

    administrative_entity = PermitAdministrativeEntitySerializer(many=False, read_only=True)

    class Meta:
        model = models.PermitRequest
        fields = ('status', 'administrative_entity', 'works_object_types')


class PermitRequestGeoTimeSerializer(gis_serializers.GeoFeatureModelSerializer):

    permit_request = PermitRequestSerializer(many=False, read_only=True)
    geom = gis_serializers.GeometryField(precision=2, remove_duplicates=True)

    class Meta:
        model = models.PermitRequestGeoTime
        geo_field = "geom"
        fields = (
            'permit_request',
            'starts_at',
            'ends_at',
            'comment',
            'external_link',
            )
