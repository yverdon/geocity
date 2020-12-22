import dataclasses
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


@dataclasses.dataclass
class WorksMetaType:
    id: int
    name: str
    label: str
    color: list


META_TYPE_CHOICES = [
    WorksMetaType (
        id=0,
        name="question-mark",
        color=[0, 140, 111, 1],
        label=_("Autres"),
    ),
    WorksMetaType (
        id=1,
        name="construction",
        color=[201, 2, 25, 1],
        label=_("Construction"),
    ),
    WorksMetaType (
        id=2,
        name="cone",
        color=[255, 166, 0, 1],
        label=_("Chantier"),
    ),
    WorksMetaType (
        id=3,
        name="sport",
        color=[39, 115, 230, 1],
        label=_("Evénement sportif"),
    ),
    WorksMetaType (
        id=4,
        name="culture",
        color=[27, 76, 150, 1],
        label=_("Evénement culturel"),
    ),
    WorksMetaType (
        id=5,
        name="commercial",
        color=[14, 36, 69, 1],
        label=_("Evénement commercial"),
    ),
    WorksMetaType (
        id=6,
        name="police",
        color=[4, 0, 255, 1],
        label=_("Dispositif de police"),
    ),
]


def meta_type_choices():

    meta_type_choices = [(k.id, k.label) for k in META_TYPE_CHOICES]

    return meta_type_choices

