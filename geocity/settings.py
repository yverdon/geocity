import os

from .admin_jazzmin_settings import JAZZMIN_SETTINGS  # noqa

# Set environment mode
ENV = os.getenv("ENV")
if ENV not in ["DEV", "PROD"]:
    raise Exception(
        f"Incorrect setting for ENV: `{ENV}`. Expecting one of `DEV` or `PROD`."
    )

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_URLCONF = "geocity.urls"
PREFIX_URL = os.environ.get("PREFIX_URL", "")
LOGIN_URL = "accounts:account_login"
LOGIN_REDIRECT_URL = "submissions:submissions_list"
LOGOUT_REDIRECT_URL = LOGIN_URL

# Name of isolated docker network used for print and pdf services. Must be unique for hosting multi
ISOLATED_NETWORK_NAME = os.getenv("ISOLATED_NETWORK_NAME")

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

CLEAR_PUBLIC_SCHEMA_ON_FIXTURIZE = os.getenv("CLEAR_PUBLIC_SCHEMA_ON_FIXTURIZE")


ENABLE_SSL = os.getenv('ENABLE_SSL', "True").lower() == "true"
if ENABLE_SSL:
    SECURE_PROXY_SSL_HEADER = (
        tuple(os.getenv("SECURE_PROXY_SSL_HEADER").split(","))
        if os.getenv("SECURE_PROXY_SSL_HEADER")
        else None
    )
    #SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# https://stackoverflow.com/a/71194288/6630397
if ENABLE_SSL:
    CSRF_TRUSTED_ORIGINS = [
        f"https://*.{os.getenv('BASE_URL')}",
        "https://*.127.0.0.1",
    ]


# This is django's default but make sure no one turns it to False
SESSION_COOKIE_HTTPONLY = True

# Highest level of security is 'Strict'
SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Strict")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# SESSION TIMEOUT
# default session time is one hour
SESSION_COOKIE_AGE = int(os.getenv("SESSION_COOKIE_AGE", 60 * 60))
SESSION_SAVE_EVERY_REQUEST = os.getenv("SESSION_SAVE_EVERY_REQUEST", True)

# LIMIT MAX CONNEXIONS ATTEMPTS
AXES_FAILURE_LIMIT = int(os.getenv("AXES_FAILURE_LIMIT", 3))
# Lock out by combination of ip AND User
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = os.getenv(
    "AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP", False
)
AXES_LOCKOUT_URL = (
    "/" + PREFIX_URL + "/account/lockout" if PREFIX_URL else "/account/lockout"
)

AXES_COOLOFF_TIME = int(os.getenv("AXES_COOLOFF_TIME", 2))

DJANGO_DOCKER_PORT = os.getenv("DJANGO_DOCKER_PORT")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if ENV == "DEV":
    DEBUG = True

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")

DATE_INPUT_FORMAT = "%d.%m.%Y"
DATETIME_INPUT_FORMAT = "%d.%m.%Y %H:%M"

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS").lower() == "true"
EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"
    if os.getenv("EMAIL_TO_CONSOLE").lower() == "false"
    else "django.core.mail.backends.console.EmailBackend"
)

DEFAULT_CHARSET = "utf-8"

# Django-Taggit
TAGGIT_CASE_INSENSITIVE = True  # make tag unique
TAGGIT_TAGS_FROM_STRING = "geocity.apps.submissions.utils.comma_splitter"

# 2FA activation
ENABLE_2FA = os.getenv("ENABLE_2FA", "false").lower() == "true"

# Allauth requirements
#  We define it here as None, since these variables will be set upon arriving to the
#  CustomLogin view.
#  It also ensures get_current_site will get the right Site, which includes a subdomain.
#  Note: Every subdomain is treated as a different Site, they require to login separately
#  See: geocity.views.SetCurrentSiteMixin(), also: settings_test.py
# FIXME: Need a default for emails sent by Crons (Cf. SubmissionInquiryClosing)
#  Or we need to add an attribute in the Submission to save the site where it has
#  been initiated.
SITE_ID = None
SITE_DOMAIN = None
# Default domain on which all forms could be made visible by any integrator
DEFAULT_SITE = os.getenv("DEFAULT_SITE")

# IBAN for UserProfile model
AUTHOR_IBAN_VISIBLE = os.getenv("AUTHOR_IBAN_VISIBLE", "false").lower() == "true"

# Allow REMOTE_USER Authentication
ALLOW_REMOTE_USER_AUTH = os.getenv("ALLOW_REMOTE_USER_AUTH", "false").lower() == "true"

SITE_HTTPS = ENV == "PROD"

# Allow CORS in DEV, needed for development of geocity_front, where the frontend domain is different
# from the django domain
if ENV == "DEV":
    SESSION_COOKIE_HTTPONLY = False
    CORS_ALLOW_CREDENTIALS = True

LOCATIONS_SEARCH_API = os.getenv("LOCATIONS_SEARCH_API")
LOCATIONS_SEARCH_API_DETAILS = os.getenv("LOCATIONS_SEARCH_API_DETAILS")

# Application definition
INSTALLED_APPS = [
    # our apps
    "geocity.apps.core",
    "geocity.apps.accounts",
    "geocity.apps.accounts.geomapfish",
    "geocity.apps.accounts.dootix",
    "geocity.apps.reports",
    "geocity.apps.forms",
    "geocity.apps.submissions",
    # dependencies
    "polymorphic",
    "adminsortable2",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "constance",
    "constance.backends.database",
    "simple_history",
    "corsheaders",
    "django_filters",
    "rest_framework",
    "rest_framework_gis",
    "knox",
    "bootstrap4",
    "bootstrap_datepicker_plus",
    "django_tables2",
    "django_tables2_column_shifter",
    "taggit",
    "oauth2_provider",
    "crispy_forms",
    "django_cron",
    "axes",
    "captcha",
    "ckeditor",
    "jazzmin",
    # django contrib apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django.contrib.sites",
    "django.contrib.postgres",
]

if ENABLE_2FA:
    INSTALLED_APPS += [
        "django_otp",
        "django_otp.plugins.otp_static",
        "django_otp.plugins.otp_totp",
        "two_factor",
    ]

if ENV == "DEV":
    INSTALLED_APPS += [
        "debug_toolbar",
        "django_extensions",
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "axes.middleware.AxesMiddleware",
]

if ENABLE_2FA:
    MIDDLEWARE += ["django_otp.middleware.OTPMiddleware"]

MIDDLEWARE += [
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

if ENV == "DEV":
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,
    ]

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_CONFIG_FIELDSETS = {
    "General Options": (
        "APPLICATION_TITLE",
        "APPLICATION_SUBTITLE",
        "APPLICATION_DESCRIPTION",
        "ALLOWED_FILE_EXTENSIONS",
        "MAX_FILE_UPLOAD_SIZE",
        "GEOCALENDAR_URL",
        "ENABLE_GEOCALENDAR",
        "ANONYMOUS_REQUEST_SENT_TITLE",
        "ANONYMOUS_REQUEST_SENT_BODY",
        "PRIVACY_POLICY_URL",
        "GENERAL_CONDITIONS_URL",
        "CONTACT_URL",
    ),
    "Theme Options": (
        "BACKGROUND_COLOR",
        "LOGIN_BACKGROUND_COLOR",
        "PRIMARY_COLOR",
        "SECONDARY_COLOR",
        "TEXT_COLOR",
        "TITLE_COLOR",
        "TABLE_COLOR",
    ),
    "Step Options": (
        "ANONYMOUS_CAPTCHA_STEP",
        "LOCATION_STEP",
        "WORKS_OBJECTS_STEP",
        "FORMS_STEP",
        "FORMS_SINGLE_STEP",
        "PROPERTIES_STEP",
        "GEO_TIME_STEP",
        "GEO_STEP",
        "TIME_STEP",
        "APPENDICES_STEP",
        "ACTORS_STEP",
        "SUBMIT_STEP",
    ),
    "API settings": (
        "IP_WHITELIST",
        "NETWORK_WHITELIST",
        "LOGOUT_REDIRECT_HOSTNAME_WHITELIST",
    ),
}

CONSTANCE_CONFIG = {
    "APPLICATION_TITLE": (
        "Demandes touchant le territoire communal",
        "Titre de la page de login",
        str,
    ),
    "APPLICATION_SUBTITLE": (
        "Petits travaux, abattages, fouilles, dépôts, etc.",
        "Sous-titre de la page de login",
        str,
    ),
    "APPLICATION_DESCRIPTION": (
        "Une application du Système d'Information du Territoire de la Ville d'Yverdon-les-Bains - mapnv.ch",
        "Description de la page de login",
        str,
    ),
    "GENERAL_CONDITIONS_URL": (
        "",
        "Lien vers les conditions générales",
        str,
    ),
    "PRIVACY_POLICY_URL": (
        "",
        "Lien vers la politique de confidentialité",
        str,
    ),
    "CONTACT_URL": (
        "",
        "Lien vers le moyen de contact (peut également être une adresse email, p. ex. mailto:info@geocity.ch)",
        str,
    ),
    "ALLOWED_FILE_EXTENSIONS": (  # Supported file extensions https://pypi.org/project/filetype/
        "pdf, jpg, png",
        "Extensions autorisées lors de l'upload de document, seuls des types images PIL et PDF sont supportés",
        str,
    ),
    "MAX_FILE_UPLOAD_SIZE": (
        10485760,
        "Taille maximum des fichiers uploadés",
        int,
    ),
    "GEOCALENDAR_URL": (
        "https://geocity.ch/app",
        "URL de l'application calendrier cartographique",
        str,
    ),
    "ENABLE_GEOCALENDAR": (
        True,
        "Définit si l'application du calendrier cartographique est utilisée ou pas (doit dans tous les cas être installée à part)",
        bool,
    ),
    "ANONYMOUS_CAPTCHA_STEP": (
        "Veuillez confirmer que vous n'êtes pas un robot",
        "",
        str,
    ),
    "ANONYMOUS_REQUEST_SENT_TITLE": ("Merci pour votre envoi", "", str),
    "ANONYMOUS_REQUEST_SENT_BODY": (
        "Nous avons bien reçu votre envoi et vous en remercions.",
        "",
        str,
    ),
    "LOCATION_STEP": ("Sélectionnez l'entité administrative", "", str),
    "WORKS_OBJECTS_STEP": ("Sélectionnez les objets", "", str),
    "FORMS_STEP": ("Sélectionnez les objets", "", str),
    "FORMS_SINGLE_STEP": ("Sélectionnez l'objet", "", str),
    "PROPERTIES_STEP": ("Renseignez les caractéristiques des objets", "", str),
    "GEO_TIME_STEP": ("Renseignez le planning et la localisation", "", str),
    "GEO_STEP": ("Renseignez la localisation", "", str),
    "TIME_STEP": ("Renseignez le planning", "", str),
    "APPENDICES_STEP": ("Ajoutez les documents", "", str),
    "ACTORS_STEP": ("Renseignez les contacts", "", str),
    "SUBMIT_STEP": ("Résumé et envoi", "", str),
    "APPLICATION_TITLE": (
        "Demandes touchant le territoire communal",
        "Titre de la page de login",
        str,
    ),
    "APPLICATION_SUBTITLE": (
        "Petits travaux, abattages, fouilles, dépôts, etc.",
        "Sous-titre de la page de login",
        str,
    ),
    "APPLICATION_DESCRIPTION": (
        "Une application du Système d'Information du Territoire de la Ville d'Yverdon-les-Bains - mapnv.ch",
        "Description de la page de login",
        str,
    ),
    "BACKGROUND_COLOR": (
        "#FFFFFF",
        "Couleur unie du fond",
        str,
    ),
    "LOGIN_BACKGROUND_COLOR": (
        "#FFFFFF",
        "Couleur unie du fond login",
        str,
    ),
    "PRIMARY_COLOR": (
        "#008c6f",
        "Couleur de thème principale",
        str,
    ),
    "SECONDARY_COLOR": (
        "#01755d",
        "Couleur de thème secondaire",
        str,
    ),
    "TEXT_COLOR": (
        "#000000",
        "Couleur du texte",
        str,
    ),
    "TITLE_COLOR": (
        "#000000",
        "Couleur du titre",
        str,
    ),
    "TABLE_COLOR": (
        "#212529",
        "Couleur du texte dans les tableaux",
        str,
    ),
    "IP_WHITELIST": (
        "172.16.0.1,172.17.0.1,127.0.0.1,localhost",
        "IP autorisées pour l'utilisation de l'API complète (/rest/submissions), séparées par des ','",
        str,
    ),
    "NETWORK_WHITELIST": (
        "172.16.0.0/12,192.168.0.0/16",
        "Réseaux autorisés pour l'utilisation de l'API complète (/rest/submissions), séparés par des ','. ATTENTION: cette valeur est aussi utilisée pour les impressions de documents, il faut donc aussi inclure le réseau utilisé par Docker.",
        str,
    ),
    "LOGOUT_REDIRECT_HOSTNAME_WHITELIST": (
        "localhost,geocity.ch",
        "Domaines autorisés à la redirection après logout",
    ),
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "constance.context_processors.config",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "geocity.context_processors.two_factor_setting",
                "geocity.apps.submissions.context_processors.step_type",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # AxesBackend
    "axes.backends.AxesBackend",
    # Classic django authentication backend
    "django.contrib.auth.backends.ModelBackend",
    # SocialAccount authentication backend with allauth
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PROVIDER_GEOMAPFISH_URL = os.getenv("AUTH_PROVIDER_GEOMAPFISH_URL", "")
AUTH_PROVIDER_DOOTIX_URL = os.getenv("AUTH_PROVIDER_DOOTIX_URL", "")

SOCIALACCOUNT_PROVIDERS = {
    "geocity.apps.accounts.geomapfish": {
        # Override SocialApp fields with an "APP" settings.
        # SocialApp object => /admin/socialaccount/socialapp.
        # Example:
        # "APP": {
        #     "client_id": "dev-liip",
        #     "secret": os.getenv("GEOMAPFISH_SECRET"),
        #     "key": "",
        #     "certificate_key": ""
        # },
        "SCOPE": ["email"],
        "VERIFIED_EMAIL": True,
    },
    "geocity.apps.accounts.dootix": {
        # Override SocialApp fields with an "APP" settings.
        # SocialApp object => /admin/socialaccount/socialapp.
        # Example:
        # "APP": {
        #     "client_id": "dev-liip",
        #     "secret": os.getenv("DOOTIX_SECRET"),
        #     "key": "",
        #     "certificate_key": ""
        # },
        "SCOPE": ["email"],
        "VERIFIED_EMAIL": True,
    },
}

# Override SocialAccountAdapter to customize User creation
SOCIALACCOUNT_FORMS = {"signup": "geocity.apps.accounts.forms.SocialSignupForm"}
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = None
ACCOUNT_SIGNUP_REDIRECT_URL = "submissions:submissions_list"
SOCIALACCOUNT_LOGIN_ON_GET = True
# Anticipate issues with upcoming 0.52.0 update
OAUTH_PKCE_ENABLED = False

BOOTSTRAP4 = {
    "include_jquery": True,
    # Avoid repeating the label in the placeholder
    "set_placeholder": False,
}

WSGI_APPLICATION = "geocity.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.getenv("PGDATABASE"),
        "USER": os.getenv("PGUSER"),
        "HOST": os.getenv("PGHOST"),
        "PORT": os.getenv("PGPORT"),
        "PASSWORD": os.getenv("PGPASSWORD"),
        "OPTIONS": {"options": "-c search_path=geocity,public"},
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

CORS_ALLOWED_ORIGINS = [] + os.getenv("ALLOWED_CORS").split(",")


if DEBUG and not CORS_ALLOWED_ORIGINS:
    CORS_ALLOW_ALL_ORIGINS = True

# Internationalization

LANGUAGE_CODE = "fr-CH"
TIME_ZONE = "Europe/Zurich"
USE_I18N = True
USE_L10N = True
USE_TZ = True

gettext = lambda x: x

LANGUAGES = (
    ("fr", gettext("French")),
    ("en", gettext("English")),
    ("de", gettext("German")),
    ("it", gettext("Italian")),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

STATIC_URL = os.environ["STATIC_URL"]
STATIC_ROOT = "/static_root"

PRIVATE_MEDIA_ROOT = "/private_documents"

ARCHIVE_ROOT = os.environ.get("ARCHIVE_ROOT", "/archive")

MIN_START_DELAY = os.getenv("MIN_START_DELAY")
WMTS_GETCAP = os.getenv("WMTS_GETCAP")
WMTS_LAYER = os.getenv("WMTS_LAYER")
WMTS_GETCAP_ALTERNATIVE = os.getenv("WMTS_GETCAP_ALTERNATIVE")
WMTS_LAYER_ALTERNATIVE = os.getenv("WMTS_LAYER_ALTERNATIVE")
OL_MAP_HEIGHT = os.getenv("OL_MAP_HEIGHT")

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework.authentication.SessionAuthentication",
        "geocity.auth.InternalTokenAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "geocity.apps.django_wfs3.pagination.CustomPagination",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        # Full API for submissions
        "submissions": os.getenv("DRF_THROTTLE_RATE_PERMITS_API"),
        # Full API for submissions_details
        "submissions_details": os.getenv("DRF_THROTTLE_RATE_PERMITS_DETAILS_API"),
        # Limited pulic API used mainly by Geocalendar front app
        "events": os.getenv("DRF_THROTTLE_RATE_EVENTS_API"),
        # Full API for search
        "search": os.getenv("DRF_THROTTLE_RATE_SEARCH_API"),
    },
}

WFS3_TITLE = "OGC API Features - Geocity"
WFS3_DESCRIPTION = "Point d'accès OGC API Features aux données Geocity."

# OAUTH2 Config
OAUTH2_PROVIDER = {
    "PKCE_REQUIRED": os.getenv("OAUTH2_PKCE_REQUIRED", "false").lower() == "true"
}

CRISPY_TEMPLATE_PACK = "bootstrap4"

CRON_CLASSES = [
    "geocity.apps.submissions.cron.SubmissionExpirationReminder",
    "geocity.apps.submissions.cron.SubmissionInquiryClosing",
]

CAPTCHA_IMAGE_SIZE = (150, 50)
CAPTCHA_FONT_SIZE = 26
TEMPORARY_USER_PREFIX = "temp_user_"
TEMPORARY_USER_ZIPCODE = 9998
ANONYMOUS_USER_ZIPCODE = 9999
ANONYMOUS_USER_PREFIX = "anonymous_user_"
ANONYMOUS_NAME = "Anonyme"
PENDING_ANONYMOUS_REQUEST_MAX_AGE = 24

if ALLOW_REMOTE_USER_AUTH:
    # Add the auth middleware
    MIDDLEWARE += ["django.contrib.auth.middleware.RemoteUserMiddleware"]

    # Remove Axes middleware and app
    MIDDLEWARE.remove("axes.middleware.AxesMiddleware")
    INSTALLED_APPS.remove("axes")

    # When using the RemoteUserBackend for intranet users override AUTHENTICATION_BACKENDS
    AUTHENTICATION_BACKENDS = [
        # Classic django authentication backend
        "django.contrib.auth.backends.RemoteUserBackend",
        "django.contrib.auth.backends.ModelBackend",
    ]

CKEDITOR_CONFIGS = {
    "default": {
        # TODO: customize style and format dropdowns
        "toolbar": "custom",
        "toolbar_custom": [
            ["Undo", "Redo"],
            ["Image", "Table", "HorizontalRule", "SpecialChar"],
            ["Bold", "Italic", "Strike", "-", "RemoveFormat"],
            [
                "NumberedList",
                "BulletedList",
                "-",
                "Outdent",
                "Indent",
                "-",
                "Blockquote",
            ],
            ["Styles", "Format"],
            ["Source"],
        ],
    },
}


def show_toolbar(request):
    """Shows the debug toolbar when `?DEBUG=true` is your URL and DEBUG is enabled."""
    return DEBUG and request.GET.get("DEBUG", "false").lower() == "true"


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "geocity.settings.show_toolbar",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

# Payment processing
PAYMENT_PROCESSING_TEST_ENVIRONMENT = (
    os.getenv("PAYMENT_PROCESSING_TEST_ENVIRONMENT", "true").lower() == "true" or DEBUG
)
PAYMENT_CURRENCY = os.getenv("PAYMENT_CURRENCY")
