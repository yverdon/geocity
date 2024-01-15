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
        "contactformforadminsite",
        "paymentsettings",
        "price",
        "formprice",
        "mapwidgetconfiguration",
    ],
    "submissions": [
        "submissionamendfield",
        "submissionworkflowstatus",
        "servicesfeestype",
    ],
    "reports": [
        "report",
        "complementarydocumenttypeforadminsite",
        "reportlayout",
        "section",
        "headerfooter",
    ],
    # FIXME: get nested submissions.payments
}

# define permissions required by integrator role

OTHER_PERMISSIONS_CODENAMES = [
    "view_user",
    "change_user",
    "view_group",
    "add_group",
    "change_group",
    "delete_group",
    "view_private_form",
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
    "read_submission",
    "amend_submission",
    "edit_submission_validations",
    "validate_submission",
    "classify_submission",
    "edit_submission",
    "view_private_form",
    "can_generate_pdf",
    "can_refund_transactions",
    "can_revert_refund_transactions",
    "can_manage_service_fee",
    # "create_service_fee",
    # "update_service_fee",
    # "delete_service_fee",
]

DEFAULT_PILOT_PERMISSION_CODENAMES = [
    "read_submission",
    "amend_submission",
    "classify_submission",
    "can_generate_pdf",
    "can_manage_service_fee",
    # "create_service_fee",
    # "update_service_fee",
    # "delete_service_fee",
]

DEFAULT_VALIDATOR_PERMISSION_CODENAMES = [
    "read_submission",
    "validate_submission",
    "can_manage_service_fee",
    # "create_service_fee",
    # "update_service_fee",
    # "delete_service_fee",
]
