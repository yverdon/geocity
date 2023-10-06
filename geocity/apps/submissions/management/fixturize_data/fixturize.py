# This file is the one used by commands.fixturize.
# Can be modified, the file is in gitignore

# Variables to change the result of the fixturize

# Defines the number of each type of user to create on each entity
iterations = {
    "integrator_iterations": 1,
    "pilot_iterations": 1,
    "validator_iterations": 1,
    "user_iterations": 1,
}

# domain:entity
# Users created (password demo) :
#   - ENTITY-superuser
#   - ENTITY-integrator-ITERATION
#   - ENTITY-pilot-ITERATION
#   - ENTITY-validator-ITERATION
#   - ENTITY-user-ITERATION
entities = {
    "first.ch": "first_entity",
    "second.ch": "second_entity",
    "third.ch": "third_entity",
    "fourth.ch": "fourth_entity",
    "fifth.ch": "fifth_entity",
}

# Geometries for the entities
geoms = [
    "SRID=2056;MultiPolygon (((2538391 1176432, 2538027 1178201, 2538485 1178804, 2537777 1179199, 2536748 1178450, 2536123 1179647, 2537382 1180593, 2537143 1181623, 2538651 1183257, 2540368 1183236, 2541252 1181093, 2541460 1180458, 2540160 1179543, 2540097 1178877, 2538391 1176432)))",
    "SRID=2056;MultiPolygon (((2543281 1184952, 2542053 1186731, 2541148 1186887, 2538214 1186367, 2537195 1184609, 2537153 1183330, 2537757 1182653, 2539317 1182404, 2543281 1184952)))",
    "SRID=2056;MultiPolygon (((2533045 1151566, 2533789 1154840, 2538236 1155380, 2541064 1154989, 2541790 1157408, 2540934 1160087, 2543074 1161259, 2546553 1159715, 2545399 1156329, 2542757 1155361, 2542348 1153798, 2542497 1152347, 2540692 1150617, 2535855 1152105, 2533045 1151566)),((2529938 1157110, 2529789 1160329, 2532245 1161557, 2532580 1160273, 2530831 1158934, 2530757 1157259, 2529938 1157110)))",
    "SRID=2056;MultiPolygon (((2553381 1146430, 2553679 1145798, 2553660 1145500, 2554777 1145296, 2555502 1145965, 2554870 1146617, 2555335 1147398, 2555037 1147417, 2554311 1146803, 2553418 1146840, 2553269 1146524, 2553381 1146430)))",
    "SRID=2056;MultiPolygon (((2538391 1176432, 2538027 1178201, 2538485 1178804, 2537777 1179199, 2536748 1178450, 2536123 1179647, 2537382 1180593, 2537143 1181623, 2538651 1183257, 2540368 1183236, 2541252 1181093, 2541460 1180458, 2540160 1179543, 2540097 1178877, 2538391 1176432)))",
]

# Ofs_ids for the entities
ofs_ids = [5938, 5938, 5586, 5890, 5938]

# Define the fields
field_comment = {
    "name": "Commentaire",
    "input_type": "text",
    "is_mandatory": False,
}
field_width = {
    "name": "Largeur [m]",
    "input_type": "number",
    "placeholder": "3",
    "help_text": "Largeur en mètres",
    "is_mandatory": False,
}
field_title = {
    "name": "Texte permettant de séparer visuellement les champs",
    "input_type": "title_output",
    "help_text": "Ce texte permet d'expliquer en détail à l'utilisateur les pourquoi et le comment des informations à fournir",
    "is_mandatory": False,
}
field_height = {
    "name": "Hauteur [m]",
    "input_type": "number",
    "placeholder": "2",
    "help_text": "Longueur en mètres",
    "is_mandatory": False,
}
field_plan = {
    "name": "Plan de situation",
    "input_type": "file",
    "help_text": "Plan complémentaire détaillant votre projet",
    "is_mandatory": False,
}
field_adresse = {
    "name": "Adresse",
    "input_type": "address",
    "placeholder": "Place Pestalozzi 2, 1400 Yverdon-les-Bains",
    "is_mandatory": False,
}
field_adresse_geocode = {
    "name": "Adresse avec géocodage",
    "input_type": "address",
    "placeholder": "Place Pestalozzi 2, 1400 Yverdon-les-Bains",
    "is_mandatory": False,
    "store_geometry_for_address_field": True,
}
field_date = {
    "name": "Date",
    "input_type": "date",
    "is_mandatory": False,
}
field_checkbox = {
    "name": "Impact sur la chaussée",
    "input_type": "checkbox",
    "is_mandatory": False,
}
field_list_single = {
    "name": "À moins de 3m d'un arbre",
    "input_type": "list_single",
    "is_mandatory": False,
    "choices": "oui\nnon",
}
field_list_multiple = {
    "name": "À moins de 3m d'un arbre",
    "input_type": "list_multiple",
    "is_mandatory": False,
    "choices": "Déviation trafic\nHoraire prolongé\nSon>90dB",
}

# Define form_categories for each entity
# To create specific cases add in front of category name :
# - RENEWAL_REMINDER
# - NO_GEOM_NOR_TIME
form_categories = [
    (
        "ADVANCED_MAP_PLUGIN Gestion participative de l'espace public",
        [
            (
                "Signaler un problème sur un lampadaire",
                field_comment,
                field_date,
            ),
        ],
    ),
    (
        "RENEWAL_REMINDER Stationnement (ex. de demande devant être prolongée)",
        [
            (
                "Demande de macaron",
                field_comment,
                field_date,
            ),
            (
                "Accès au centre-ville historique",
                field_plan,
                field_width,
                field_comment,
                field_title,
                field_date,
                field_checkbox,
                field_adresse,
                field_list_multiple,
            ),
        ],
    ),
    (
        "Événements sur la voie publique",
        [
            (
                "Événement sportif",
                field_plan,
                field_width,
                field_comment,
                field_title,
                field_date,
                field_checkbox,
                field_adresse,
                field_list_multiple,
            ),
            (
                "Événement culturel",
                field_plan,
                field_width,
                field_comment,
                field_title,
                field_date,
                field_checkbox,
                field_adresse,
                field_list_multiple,
            ),
            (
                "Événement politique",
                field_plan,
                field_width,
                field_comment,
                field_title,
                field_date,
                field_checkbox,
                field_adresse,
                field_list_multiple,
            ),
            (
                "Événement commercial",
                field_plan,
                field_width,
                field_comment,
                field_title,
                field_date,
                field_checkbox,
                field_adresse,
                field_list_multiple,
            ),
        ],
    ),
    (
        "Chantier",
        [
            (
                "Permis de fouille",
                field_width,
                field_height,
                field_title,
                field_comment,
                field_adresse,
                field_adresse_geocode,
                field_checkbox,
                field_list_single,
            ),
            (
                "Permis de dépôt",
                field_width,
                field_height,
                field_comment,
                field_title,
                field_adresse,
                field_adresse_geocode,
                field_checkbox,
            ),
        ],
    ),
    (
        "NO_GEOM_NOR_TIME Subventions (ex. de demande sans géométrie ni période temporelle)",
        [
            (
                "Prime éco-mobilité",
                field_comment,
            ),
            (
                "Abonnement de bus",
                field_comment,
            ),
        ],
    ),
]

form_additional_information = """
Texte expliquant la ou les conditions particulière(s) s'appliquant à cette demande.
Un document pdf peut également être proposé à l'utilisateur, par exemple pour les conditions
de remise en état après une fouille sur le domaine public
"""

small_text = """
On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure
of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to
those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases
are perfectly simple and easy to distinguish."""

# Advanced map config example

advanced_map_config = {
    "wfs": {
        "url": "https://mapnv.ch/mapserv_proxy?ogcserver=source+for+image%2Fpng&SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=ELE_tragwerk_gesco"
    },
    "mode": {"type": "mix"},
    "wmts": [
        {
            "name": "",
            "layer": "ch.swisstopo.swissimage",
            "thumbnail": "/static/images/aerial.svg",
            "capability": "https://wmts.geo.admin.ch/EPSG/2056/1.0.0/WMTSCapabilities.xml",
            "projection": "EPSG:2056",
        }
    ],
    "zoom": 15,
    "border": {
        "url": "",
        "notification": "Veuillez placer votre élément dans les limites autorisées",
    },
    "search": {
        "displaySearch": True,
        "bboxRestiction": "",
        "requestWithoutCustomValue": "https://api3.geo.admin.ch/rest/services/api/SearchServer?limit=5&&type=locations&sr=2056&lang=fr&origins=address%2Cparcel",
    },
    "cluster": {"distance": 40, "minDistance": 35},
    "maxZoom": 20,
    "minZoom": 1,
    "information": {"title": "Signaler ...", "content": "", "duration": 5000},
    "interaction": {
        "fullscreen": True,
        "displayZoom": True,
        "enableRotation": True,
        "displayScaleLine": False,
        "enableGeolocation": True,
        "enableCenterButton": True,
    },
    "outputFormat": "GeometryCollection",
    "defaultCenter": [2539057, 1181111],
    "inclusionArea": {"url": "", "filter": ""},
    "notifications": [
        {
            "rule": {
                "type": "ZOOM_CONSTRAINT",
                "minZoom": 16,
                "maxElement": None,
                "couldBypass": None,
            },
            "type": "warning",
            "message": "Veuillez zoomer davantage avant de pouvoir sélectionner un emplacement.",
        },
        {
            "rule": {
                "type": "MAX_SELECTION",
                "minZoom": None,
                "maxElement": 1,
                "couldBypass": None,
            },
            "type": "warning",
            "message": "Le maximum de sélection est limité à {x}.",
        },
        {
            "rule": {
                "type": "INFORMATION",
                "minZoom": None,
                "maxElement": None,
                "couldBypass": None,
            },
            "type": "info",
            "message": "Sélectionnez un marqueur ou cliquez longuement sur la carte pour qu’un élément soit créé.",
        },
    ],
    "geolocationInformation": {
        "displayBox": True,
        "currentLocation": False,
        "reverseLocation": True,
    },
    "selectionTargetBoxMessage": "",
}
