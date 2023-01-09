from django.conf import settings

INTEGRATOR_PERMISSIONS_BY_APP = {
    "accounts": [
        "permitdepartment",
        "userprofile",
    ],
    "forms": [
        "administrativeentityforadminsite",
        "formcategory",
        "form",
        "field",
        "formfield",
        "contacttypeforadminsite",
        "paymentsettings",
        "price",
    ],
    "submissions": [
        "submissionamendfield",
        "submissionworkflowstatus",
    ],
    "reports": [
        "report",
        "complementarydocumenttypeforadminsite",
        "reportlayout",
        "section",
    ],
}

# define permissions required by integrator role
# TODO this is kept for backwards compatibility with migrations of the legacy `permits`
# app. Once the final migration of this app has been applied and all associated code of
# this app has been removed, remove this line
INTEGRATOR_REQUIRED_MODELS_PERMISSIONS = []

OTHER_PERMISSIONS_CODENAMES = [
    "view_user",
    "change_user",
    "view_group",
    "add_group",
    "change_group",
    "delete_group",
    "view_private_submission",
]

if not settings.ALLOW_REMOTE_USER_AUTH:
    # Django axes
    OTHER_PERMISSIONS_CODENAMES += [
        "add_accessattempt",
        "change_accessattempt",
        "delete_accessattempt",
        "view_accessattempt",
    ]

AVAILABLE_FOR_INTEGRATOR_PERMISSION_CODENAMES = [
    "amend_submission",
    "validate_submission",
    "classify_submission",
    "edit_submission",
    "view_private_submission",
    "can_generate_pdf",
    "can_refund_transactions",
    "can_revert_refund_transactions",
]
