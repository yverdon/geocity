import os

# from jazzmin_settings import JAZZMIN_SETTINGS

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


SECURE_PROXY_SSL_HEADER = (
    tuple(os.getenv("SECURE_PROXY_SSL_HEADER").split(","))
    if os.getenv("SECURE_PROXY_SSL_HEADER")
    else None
)

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
    "geocity.apps.permits",
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
        "WORKS_TYPES_STEP",
        "WORKS_OBJECTS_STEP",
        "PROPERTIES_STEP",
        "GEO_TIME_STEP",
        "TIME_STEP",
        "GEO_STEP",
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
        "URL vers la politique de confidentialité",
        str,
    ),
    "PRIVACY_POLICY_URL": (
        "",
        "URL vers la politique de confidentialité",
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
    "LOCATION_STEP": ("Sélectionnez la commune / l'entité", "", str),
    "WORKS_TYPES_STEP": ("Sélectionnez le ou les type(s)", "", str),
    "WORKS_OBJECTS_STEP": ("Sélectionnez les objets", "", str),
    "PROPERTIES_STEP": ("Renseignez les caractéristiques des objets", "", str),
    "GEO_TIME_STEP": ("Renseignez le planning et la localisation", "", str),
    "TIME_STEP": ("Renseignez le planning", "", str),
    "GEO_STEP": ("Renseignez la localisation", "", str),
    "APPENDICES_STEP": ("Ajouter des documents", "", str),
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
        "Réseaux autorisés pour l'utilisation de l'API complète (/rest/submissions), séparés par des ','",
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


JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Geocity",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Geocity",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Geocity",

    # Logo to use for your site, must be present in static files, used for brand on top left
    # "site_logo": "books/img/logo.png",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": None,

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": "Bienvenue sur le site d'administration de Geocity",

    # Copyright on the footer
    "copyright": "Geocity-asso",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string 
    "search_model": ["auth.User", "auth.Group"],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", },

        # external url that opens in a new window (Permissions can be added)
        {"name": "Support", "url": "https://github.com/yverdon/geocity/wiki", "new_window": True},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"model": "auth.user"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["auth", "accounts", "forms", "submissions", "reports",],

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "accounts.AdministrativeEntity": "fas fa-building",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": True,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": False,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "single",
    # override change forms on a per modeladmin basis
    # "changeform_format_overrides": {"auth.user": "single", "auth.group": "single", "forms.proxyadministrativeentity": "single"},
    # Add a language dropdown into the admin
    # "language_chooser": True,
}