from constance import config
from urllib import parse
from permits import models
from django.conf import settings


def get_wot_properties(value):
    obj = value.all()
    wot_props = obj.values(
        "properties__property__name",
        "properties__value__val",
        "works_object_type_id",
        "works_object_type__works_object__name",
        "works_object_type__works_type__name",
    )
    wot_properties = {}

    if wot_props:
        for prop in wot_props:
            wot = f'{prop["works_object_type__works_object__name"]} ({prop["works_object_type__works_type__name"]})'
            wot_properties[wot] = {
                prop_i["properties__property__name"]: prop_i["properties__value__val"]
                for prop_i in wot_props
                if prop_i["works_object_type_id"] == prop["works_object_type_id"]
                and prop_i["properties__property__name"]
            }
    return wot_properties


def get_amend_properties(value):
    obj = value.all()
    amend_props = obj.values(
        "amend_properties__property__name",
        "amend_properties__value",
        "works_object_type_id",
        "works_object_type__works_object__name",
        "works_object_type__works_type__name",
    )
    amend_properties = {}

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

    return amend_properties
