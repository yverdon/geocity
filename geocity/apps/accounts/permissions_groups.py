from django.conf import settings


INTEGRATOR_ACCOUNTS_MODELS_PERMISSIONS = [
    "administrativeentity",
    "permitdepartment",
    "userprofile",
]
INTEGRATOR_FORMS_MODELS_PERMISSIONS = [
    "formcategory",
    "form",
    "field",
]
INTEGRATOR_SUBMISSIONS_MODELS_PERMISSIONS = [
    "contacttype",       
    "submissionamendfield",
    "submissionworkflowstatus",
    "complementarydocumenttype",
]
INTEGRATOR_REPORTS_MODELS_PERMISSIONS = [
    "report",
    "reportlayout",
    "section",
]

# define permissions required by integrator role
INTEGRATOR_REQUIRED_MODELS_PERMISSIONS = [
    INTEGRATOR_ACCOUNTS_MODELS_PERMISSIONS,
    INTEGRATOR_FORMS_MODELS_PERMISSIONS,
    INTEGRATOR_SUBMISSIONS_MODELS_PERMISSIONS,
]

OTHER_PERMISSIONS_CODENAMES = [
    "view_user",
    "change_user",
    "view_group",
    "add_group",
    "change_group",
    "delete_group",
    "see_private_requests",
]

if not settings.ALLOW_REMOTE_USER_AUTH:
    # Django axes
    OTHER_PERMISSIONS_CODENAMES += [
        "add_accessattempt",
        "change_accessattempt",
        "delete_accessattempt",
        "view_accessattempt",
        "add_accesslog",
        "change_accesslog",
        "delete_accesslog",
        "view_accesslog",
    ]


AVAILABLE_FOR_INTEGRATOR_PERMISSION_CODENAMES = [
    "amend_permit_request",
    "validate_permit_request",
    "classify_permit_request",
    "edit_permit_request",
    "see_private_requests",
    "can_generate_pdf",
]
