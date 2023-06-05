import json
from collections import OrderedDict
from datetime import timedelta

from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Max, Min
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from geocity import geometry, settings
from geocity.apps.accounts.models import AdministrativeEntity, UserProfile
from geocity.apps.submissions import search
from geocity.apps.submissions.models import (
    FieldValue,
    Submission,
    SubmissionComplementaryDocument,
    SubmissionGeoTime,
)
from geocity.apps.submissions.payments.models import SubmissionPrice
from geocity.apps.submissions.payments.postfinance.models import PostFinanceTransaction


def get_field_value_based_on_field(prop):
    property_object = FieldValue.objects.get(
        field_id=prop["field_values__field_id"],
        selected_form_id=prop["id"],
    )

    return property_object.get_value()


def get_form_fields(
    value,
    administrative_entities_associated_to_user_list=None,
    current_user=None,
    value_with_type=False,
):
    """
    Return form fields in a list for the api, in a dict for backend
    `value` is a query set of SelectedForm objects.
    """
    obj = value.all()
    wot_props = obj.values(
        "field_values__field__name",
        "field_values__field_id",
        "field_values__field__input_type",
        "field_values__value__val",
        "form_id",
        "id",
        "form__name",
        "form__category__name",
        "field_values__field__is_public_when_permitrequest_is_public",
        "submission__administrative_entity",
        "submission__author",
    )

    wot_properties = dict()
    property = list()
    last_wot = ""

    if wot_props:
        # Flat view is used in the api for geocalendar, the WOT shows only the works_object__name and not the type
        if value_with_type:
            wot_properties = list()
            key_for_form = _("Formulaire")
            for prop in wot_props:
                wot = prop["form__name"] + (
                    f' ({prop["form__category__name"]})'
                    if prop["form__category__name"]
                    else ""
                )

                # List of a list, to split wot in objects. Check if last wot changed or never assigned. Means it's first iteration
                if property and wot != last_wot:
                    # Don't add values if there's only the "WOT" without any field
                    if len(property) > 1:
                        wot_properties.append(property)

                    property = []
                    # WOT
                    property.append(
                        {
                            "key": key_for_form,
                            "value": wot,
                            "type": "text",
                        }
                    )

                if not last_wot:
                    property.append(
                        {
                            "key": key_for_form,
                            "value": wot,
                            "type": "text",
                        }
                    )

                last_wot = wot

                # Show fields_values only when the current submission__administrative_entity
                # is one of the administrative_entities associated to the user
                # or user is the submission__author
                # or show field_values that are designed as public in a public permit_request
                if prop["field_values__field__input_type"] == "file" and (
                    (
                        administrative_entities_associated_to_user_list
                        and prop["submission__administrative_entity"]
                        in administrative_entities_associated_to_user_list
                    )
                    or (current_user and prop["submission__author"] == current_user.id)
                    or prop[
                        "field_values__field__is_public_when_permitrequest_is_public"
                    ]
                ):
                    # get_property_value return None if file does not exist
                    file = get_field_value_based_on_field(prop)
                    # Check if file exist
                    if file:
                        # Properties of WOT
                        property.append(
                            {
                                "key": prop["field_values__field__name"],
                                "value": file.url,
                                "type": prop["field_values__field__input_type"],
                            }
                        )
                elif prop["field_values__value__val"] and (
                    (
                        administrative_entities_associated_to_user_list
                        and prop["submission__administrative_entity"]
                        in administrative_entities_associated_to_user_list
                    )
                    or (current_user and prop["submission__author"] == current_user.id)
                    or prop[
                        "field_values__field__is_public_when_permitrequest_is_public"
                    ]
                ):
                    # Properties of WOT
                    property.append(
                        {
                            "key": prop["field_values__field__name"],
                            "value": prop["field_values__value__val"],
                            "type": prop["field_values__field__input_type"],
                        }
                    )
            # Add last wot_properties, or show something when there's only one
            # Don't add values if there's only the "WOT" without any field
            if len(property) > 1:
                wot_properties.append(property)
        else:
            for prop in wot_props:
                wot = f'{prop["form__name"]} ({prop["form__category__name"]})'
                wot_properties[wot] = {
                    prop_i["field_values__field__name"]: get_field_value_based_on_field(
                        prop_i
                    ).url
                    # Check this is a file and the file exist
                    if prop_i["field_values__field__input_type"] == "file"
                    and get_field_value_based_on_field(prop_i)
                    else prop_i["field_values__value__val"]
                    for prop_i in wot_props
                    if prop_i["form_id"] == prop["form_id"]
                    and prop_i["field_values__field__name"]
                }
    return wot_properties


def get_amend_properties(value):
    # `value` here is QuerySet[SelectedForm]
    obj = value.all()
    amend_fields = obj.values(
        "amend_fields__field__name",
        "amend_fields__value",
        "form_id",
        "form__name",
        "form__category__name",
    )
    amend_properties = {}

    for field in amend_fields:
        amends = f'{field["form__name"]} ({field["form__category__name"]})'
        amend_properties[amends] = {
            prop_i["amend_fields__field__name"]: prop_i["amend_fields__value"]
            for prop_i in amend_fields
            if prop_i["form_id"] == field["form_id"]
            and prop_i["amend_fields__field__name"]
        }

    return amend_properties


class AdministrativeEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeEntity
        fields = (
            "id",
            "name",
            "ofs_id",
            "link",
            "phone",
        )


class MetaTypesField(serializers.RelatedField):
    def to_representation(self, value):
        meta_types = {form.category.meta_type for form in value.all()}
        return list(meta_types)


class FormsNames(serializers.RelatedField):
    def to_representation(self, value):
        forms_names = {
            form.id: form.name
            + (f" ({form.category.name})" if form.category_id else "")
            for form in value.all()
        }
        return forms_names


class SubmissionComplementaryDocumentSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField()

    def get_uri(self, document):
        request = self.context.get("request")
        return request.build_absolute_uri(document.uri)

    class Meta:
        model = SubmissionComplementaryDocument

        fields = (
            "name",
            "uri",
        )


class SubmissionInquirySerializer(serializers.ModelSerializer):
    documents = SubmissionComplementaryDocumentSerializer(read_only=True, many=True)

    class Meta:
        fields = (
            "id",
            "start_date",
            "end_date",
            "documents",
        )


class SubmissionPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionPrice
        fields = (
            "text",
            "amount",
            "currency",
        )


class PostFinanceTransactionPrintSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        repr = super(PostFinanceTransactionPrintSerializer, self).to_representation(
            instance
        )
        repr["creation_date"] = instance.creation_date.strftime("%d.%m.%Y")
        repr["creation_date_year"] = instance.creation_date.strftime("%Y")
        repr[
            "line_text"
        ] = instance.submission_price.submission.get_form_for_payment().name
        return repr

    class Meta:
        model = PostFinanceTransaction
        fields = (
            "merchant_reference",
            "amount",
            "currency",
            "creation_date",
        )


class SentDateSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.strftime("%d.%m.%Y %H:%M")


class SubmissionSerializer(serializers.ModelSerializer):
    administrative_entity = AdministrativeEntitySerializer(read_only=True)
    meta_types = MetaTypesField(source="forms", read_only=True)
    forms_names = FormsNames(source="forms", read_only=True)
    current_inquiry = SubmissionInquirySerializer(
        source="submission__inquiry", read_only=True
    )  # perf leek 1
    price = SubmissionPriceSerializer(read_only=True)
    sent_date = SentDateSerializer(read_only=True)  # perf leak 3

    class Meta:
        model = Submission
        fields = (
            "id",
            "status",
            "shortname",
            "administrative_entity",
            "forms",
            "meta_types",
            "forms_names",
            "current_inquiry",
            "price",
            "sent_date",
        )


class FieldsValuesSerializer(serializers.RelatedField):
    def to_representation(self, value):
        current_user = None
        request = self.context.get("request", None)
        if request:
            current_user = request.user
            session_authentication = request.session._SessionBase__session_key
        else:
            current_user = None
            session_authentication = None

        # User is logged by session_authentication
        user_is_authenticated = (
            current_user and current_user.is_authenticated and session_authentication
        )

        administrative_entities_associated_to_user_list = None

        if user_is_authenticated:
            administrative_entities_associated_to_user_list = (
                AdministrativeEntity.objects.associated_to_user(request.user)
                .values_list("id", flat=True)
                .distinct()
            )

        fields = get_form_fields(
            value,
            administrative_entities_associated_to_user_list,
            current_user,
            value_with_type=True,
        )
        return fields


class SelectedFormSerializer(serializers.RelatedField):
    def to_representation(self, value):
        fields = get_form_fields(value)
        amend_fields = get_amend_properties(value)

        form_and_amend_fields = {
            "submission_fields": fields,
            "amend_fields": amend_fields,
        }
        return form_and_amend_fields


class SubmissionContactSerializer(serializers.Serializer):
    def to_representation(self, value):
        rep = {}
        for submission_contact in value.submission_contacts.select_related("contact"):
            contact_object = {
                "contact_type_display": submission_contact.get_contact_type_display()
            }
            for field in submission_contact.contact._meta.fields:
                contact_object[field.name] = getattr(
                    submission_contact.contact, field.name
                )
            rep[submission_contact.get_contact_type_display()] = contact_object

        return rep


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    email = serializers.ReadOnlyField(source="user.email")
    user_id = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = UserProfile
        fields = (
            "first_name",
            "last_name",
            "address",
            "zipcode",
            "user_id",
            "city",
            "company_name",
            "vat_number",
            "iban",
            "phone_first",
            "phone_second",
            "email",
        )


class CurrentUserSerializer(serializers.Serializer):
    def to_representation(self, value):
        if value.is_authenticated:
            json = {
                "is_logged": True,
                "username": value.username,
                "email": value.email,
                "login_datetime": value.last_login.strftime("%Y-%m-%d %H:%M:%S"),
                "expiration_datetime": (
                    value.last_login + timedelta(seconds=settings.SESSION_COOKIE_AGE)
                ).strftime("%Y-%m-%d %H:%M:%S"),
            }
        else:
            json = {
                "is_logged": False,
            }

        return json


class SubmissionValidationSerializer(serializers.Serializer):
    def to_representation(self, value):
        rep = {}
        for validation in value.validations.all().select_related("department"):
            values = {}
            for field in validation._meta.fields:
                values["validation_status"] = validation.get_validation_status_display()
                if (
                    field.name == "comment"
                    or field.name == "comment_is_visible_by_author"
                ):
                    values[field.name] = getattr(validation, field.name)

            rep[validation.department.group.name] = values
        return rep


class SubmissionGeoTimeSerializer(gis_serializers.GeoFeatureModelSerializer):
    submission = SubmissionSerializer(read_only=True)

    class Meta:
        model = SubmissionGeoTime
        geo_field = "geom"
        auto_bbox = True
        fields = (
            "submission",
            "starts_at",
            "ends_at",
            "comment",
            "external_link",
        )


class SubmissionGeoTimeGeoJSONSerializer(serializers.Serializer):
    """
    In order to serialize the object as a GeoJSON a queryset has to be passed,
    however, the queryset could have many geometry types in a single row as well as
    many rows with different geometries, in order to generate a single layer from
    all the possible results, the geometries have to be aggregated.

    Note: Here we need the geo_time queryset as the source (value), since the
    geometry and the dates will be aggregated, but the comments
    and external links will be retrieved and grouped from it.

    Note: The extract_geom parameter specifies the aggregation function used to represent
    the geometries. If not specified, it will return a bounding box. If specified, it
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
                geom_function = geometry.ExtractPoints("geom")
            elif self.extract_geom == self.EXTRACT_LINES:
                geom_function = geometry.ExtractLines("geom")
            elif self.extract_geom == self.EXTRACT_POLYS:
                geom_function = geometry.ExtractPolys("geom")
            else:
                geom_function = geometry.JoinGeometries("geom")

            aggregated_geotime_qs = geo_time_qs.values("submission_id").aggregate(
                submission_geo_time_end_date=Max("ends_at"),
                submission_geo_time_start_date=Min("starts_at"),
                singlegeom=geom_function,
            )

            result = {"properties": {}}
            if not aggregated_geotime_qs["singlegeom"]:
                result["geometry"] = {"type": "Polygon", "coordinates": []}
            else:
                result["geometry"] = json.loads(
                    GEOSGeometry(aggregated_geotime_qs["singlegeom"]).json
                )

            geotime_aggregated = {}
            geotime_aggregated["start_date"] = (
                aggregated_geotime_qs["submission_geo_time_start_date"].strftime(
                    "%d.%m.%Y %H:%M"
                )
                if aggregated_geotime_qs["submission_geo_time_start_date"]
                else ""
            )
            geotime_aggregated["end_date"] = (
                aggregated_geotime_qs["submission_geo_time_end_date"].strftime(
                    "%d.%m.%Y %H:%M"
                )
                if aggregated_geotime_qs["submission_geo_time_end_date"]
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


# Override of real ListSerializer from django-rest-framework-gis
# If you want to add a new structure with dynamic values, just add it to OrderedDict and give him a new function like "super().prefix_to_representation(data)"
# Then in SubmissionPrintSerializer write this class like the existant "to_representation"
class SubmissionPrintListSerialier(gis_serializers.ListSerializer):
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


class SubmissionPrintSerializer(gis_serializers.GeoFeatureModelSerializer):
    submission = SubmissionSerializer(source="*", read_only=True)
    form_and_amend_fields = SelectedFormSerializer(
        source="selected_forms", read_only=True
    )
    contacts = SubmissionContactSerializer(source="*", read_only=True)
    geo_envelop = SubmissionGeoTimeGeoJSONSerializer(
        source="geo_time",
        read_only=True,
    )

    creditor_type = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    author = UserProfileSerializer(
        read_only=True, source="author.userprofile", default=None
    )
    validations = SubmissionValidationSerializer(source="*", read_only=True)

    def get_creditor_type(self, obj):
        if obj.creditor_type is not None:
            creditor = obj.get_creditor_type_display()
        elif obj.author:
            creditor = (
                _("Auteur de la demande, ")
                + f"{obj.author.first_name} {obj.author.last_name}"
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
        model = Submission
        geo_field = "geo_time"
        id_field = "id"
        fields = (
            "id",
            "submission",
            "additional_decision_information",
            "form_and_amend_fields",
            "contacts",
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
            meta, "list_serializer_class", SubmissionPrintListSerialier
        )
        return list_serializer_class(*args, **list_kwargs)

    def to_representation(self, value):
        rep = super().to_representation(value)

        # If the WOT has no geometry, we add the centroid of the administrative entity as a square (polygon)
        if rep["properties"]["geo_envelop"]["geometry"]["coordinates"] == []:
            administrative_entity_id = rep["properties"]["submission"][
                "administrative_entity"
            ]["id"]
            administrative_entity = (
                AdministrativeEntity.objects.filter(id=administrative_entity_id)
                .annotate(centroid_geom=geometry.JoinGeometries("geom"))
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
        for field, value in rep["properties"]["submission"].items():
            rep["properties"][f"submission_{field}"] = value
        del rep["properties"]["submission"]

        # Flattening the rest of related properties
        related_fields_to_flatten = ["form_and_amend_fields"]

        for field_to_flatten in related_fields_to_flatten:
            for field, value in rep["properties"][field_to_flatten].items():
                rep["properties"][field] = value
            del rep["properties"][field_to_flatten]
        return rep


class SubmissionDetailsSerializer(serializers.ModelSerializer):
    fields_values = FieldsValuesSerializer(source="selected_forms", read_only=True)

    class Meta:
        model = Submission
        fields = (
            "id",
            "fields_values",
        )


class SubmissionFiltersSerializer(serializers.Serializer):
    form = serializers.IntegerField(default=None, allow_null=True)
    status = serializers.ChoiceField(
        Submission.STATUS_CHOICES, default=None, allow_null=True
    )
    geom_type = serializers.ChoiceField(
        ("lines", "points", "polygons"), default=None, allow_null=True
    )
    submission_id = serializers.IntegerField(default=None, allow_null=True)


class SearchSerializer(serializers.Serializer):
    def to_representation(self, value):
        return search.search_result_to_json(value)
