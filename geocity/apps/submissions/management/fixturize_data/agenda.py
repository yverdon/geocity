# This file is the one used by commands.fixturize.
# Can be modified, the file is in gitignore

# Variables to change the result of the fixturize

# Defines the number of each type of user to create on each entity
iterations = {
    "integrator_iterations": 1,
    "pilot_iterations": 1,
    "validator_iterations": 1,
    "user_iterations": 40,
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
}

# Geometries for the entities
geoms = [
    "SRID=2056;MultiPolygon (((2538391 1176432, 2538027 1178201, 2538485 1178804, 2537777 1179199, 2536748 1178450, 2536123 1179647, 2537382 1180593, 2537143 1181623, 2538651 1183257, 2540368 1183236, 2541252 1181093, 2541460 1180458, 2540160 1179543, 2540097 1178877, 2538391 1176432)))",
]

# Ofs_ids for the entities
ofs_ids = [5938]

# Define the fields
field_title = {
    "name": "Title",
    "input_type": "text",
    "is_mandatory": True,
    "api_light": True,
    "public_if_submission_public": True,
}
field_location = {
    "name": "Location",
    "input_type": "text",
    "is_mandatory": True,
    "api_light": True,
    "public_if_submission_public": True,
}
field_location_details = {
    "name": "Location details",
    "input_type": "text",
    "is_mandatory": True,
    "api_light": False,
    "public_if_submission_public": True,
}
field_summary = {
    "name": "Summary",
    "input_type": "text",
    "is_mandatory": True,
    "api_light": False,
    "public_if_submission_public": True,
}
field_Pricing = {
    "name": "Pricing",
    "input_type": "text",
    "is_mandatory": True,
    "api_light": False,
    "public_if_submission_public": True,
}
field_website = {
    "name": "Website",
    "input_type": "text",
    "is_mandatory": True,
    "api_light": False,
    "public_if_submission_public": True,
}
field_schedule = {
    "name": "Schedule",
    "input_type": "text",
    "is_mandatory": True,
    "api_light": False,
    "public_if_submission_public": True,
}
field_organizer_name = {
    "name": "Organizer name",
    "input_type": "text",
    "is_mandatory": True,
    "api_light": False,
    "public_if_submission_public": True,
}
field_organizer_address = {
    "name": "Organizer address",
    "input_type": "text",
    "is_mandatory": True,
    "api_light": False,
    "public_if_submission_public": True,
}
field_organizer_phone = {
    "name": "Organizer phone",
    "input_type": "text",
    "is_mandatory": True,
    "api_light": False,
    "public_if_submission_public": True,
}
field_organizer_email = {
    "name": "Organizer email",
    "input_type": "text",
    "is_mandatory": True,
    "api_light": False,
    "public_if_submission_public": True,
}
field_organizer_website = {
    "name": "Organizer website",
    "input_type": "text",
    "is_mandatory": True,
    "api_light": False,
    "public_if_submission_public": True,
}
field_publics = {
    "name": "Publics",
    "input_type": "list_multiple",
    "is_mandatory": True,
    "api_light": False,
    "public_if_submission_public": True,
    "filter_for_api": True,
    "choices": "Tous publics\nFamilles\nJeunes\nSeniors",
}
field_regions = {
    "name": "Régions",
    "input_type": "list_single",
    "is_mandatory": True,
    "api_light": False,
    "public_if_submission_public": True,
    "filter_for_api": True,
    "choices": "Grandson\nOrbe\nRomainmôtier\nSainte-Croix\nVallée de Joux\nVallorbe\nYverdon\nYvonand",
}
field_types = {
    "name": "Types",
    "input_type": "list_multiple",
    "is_mandatory": True,
    "api_light": False,
    "public_if_submission_public": True,
    "filter_for_api": True,
    "choices": "Concert\nSpectacle\nExposition\nFestival\nAtelier, Animation & Médiation\nPerformance\nInstallation\nCompétition",
}
field_domaines = {
    "name": "Domaines",
    "input_type": "list_multiple",
    "is_mandatory": True,
    "api_light": False,
    "public_if_submission_public": True,
    "filter_for_api": True,
    "choices": "Art vivant\nArt visuel\nAudiovisuel\nPatrimoine & Architecture\nMusique\nLittérature\nArtisanat & Tradition\nSport",
}
field_poster = {
    "name": "Poster",
    "input_type": "file",
    "is_mandatory": False,
    "api_light": True,
    "public_if_submission_public": True,
}
field_non_public = {
    "name": "Champ pas public, ne doit pas s'afficher dans l'api et l'agenda",
    "input_type": "text",
    "is_mandatory": False,
    "api_light": True,
    "public_if_submission_public": False,
}

# Define form_categories for each entity
# To create specific cases add in front of category name :
# - RENEWAL_REMINDER
# - NO_GEOM_NOR_TIME
form_categories = [
    (
        "AGENDA Agenda - Sports",
        [
            (
                "Agenda - Sports",
                field_title,
                field_location,
                field_location_details,
                field_summary,
                field_Pricing,
                field_website,
                field_schedule,
                field_organizer_name,
                field_organizer_address,
                field_organizer_phone,
                field_organizer_email,
                field_organizer_website,
                field_publics,
                field_regions,
                field_types,
                field_domaines,
                field_poster,
                field_non_public,
            ),
        ],
    ),
    (
        "AGENDA Agenda - Culture",
        [
            (
                "Agenda - Culture",
                field_title,
                field_location,
                field_location_details,
                field_summary,
                field_Pricing,
                field_website,
                field_schedule,
                field_organizer_name,
                field_organizer_address,
                field_organizer_phone,
                field_organizer_email,
                field_organizer_website,
                field_publics,
                field_regions,
                field_types,
                field_domaines,
                field_poster,
                field_non_public,
            ),
        ],
    ),
]

form_additional_information = """
Texte expliquant la ou les conditions particulière(s) s'appliquant à cette demande.
Un document pdf peut également être proposé à l'utilisateur, par exemple pour les conditions
de remise en état après une fouille sur le domaine public
"""

small_text = "This is a small text"

images_folder = "posters"
