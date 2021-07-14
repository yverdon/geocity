# Mapnv profile_url success response mock.
# Happen if login succeeded.
# That's all the data we can get from MAPNV.
profile_response_mock = {
    "username": "liip",
    "email": "olm@ylb.ch",
    "functionalities": {
        "default_basemap": [],
        "default_theme": [],
        "filterable_layers": [
            "station_armoire_depart",
            "ELE_tube",
            "VD_batiment_rcb",
            "qwat_conduites",
            "YLB - Gestion des surface par service responsable",
            "qgep_conduites",
            "WAS_conduite",
            "MO_bf_bien_fonds",
            "ELE_branchement_immeuble",
            "GAS_conduite_bp",
        ],
        "open_panel": [],
        "preset_layer_filter": [],
        "print_template": [
            "2 A4 Portrait",
            "4 A3 Portrait",
            "3 A3 Paysage",
            "6 A1 Paysage",
            "5 A2 Paysage",
            "1 A4 Paysage",
            "8 A5 Paysage",
        ],
    },
    "is_intranet": False,
    "roles": [{"id": 2, "name": "role_yverdon"}],
    "two_factor_enable": False,
}
