import os

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_URLCONF = "geomapshark.urls"
PREFIX_URL = os.environ.get("PREFIX_URL", "")
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "permits:permit_requests_list"
LOGOUT_REDIRECT_URL = LOGIN_URL

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

# Set environment mode
ENV = os.getenv("ENV")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if ENV.lower() == "dev":
    DEBUG = True

os.environ["GDAL_DATA"] = os.path.join(BASE_DIR, "gdal_data")
GDAL_DATA = os.environ["GDAL_DATA"]
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
TAGGIT_TAGS_FROM_STRING = "permits.utils.comma_splitter"

# 2FA activation
ENABLE_2FA = os.getenv("ENABLE_2FA", "false").lower() == "true"

# Allow REMOTE_USER Authentication
ALLOW_REMOTE_USER_AUTH = os.getenv("ALLOW_REMOTE_USER_AUTH", "false").lower() == "true"

# Allauth requirement
SITE_ID = 1
SITE_DOMAIN = os.getenv("SITE_DOMAIN", "localhost")
SITE_HTTPS = bool(int(os.getenv("SITE_HTTPS", True)))

# Application definition
INSTALLED_APPS = [
    "adminsortable2",
    "grappelli",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django.contrib.sites",
    "django.contrib.postgres",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "accounts.geomapfish",
    "accounts.dootix",
    "constance",
    "constance.backends.database",
    "simple_history",
    "corsheaders",
    "django_filters",
    "rest_framework",
    "rest_framework_gis",
    "rest_framework.authtoken",
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
]

if ENABLE_2FA:
    INSTALLED_APPS += [
        "django_otp",
        "django_otp.plugins.otp_static",
        "django_otp.plugins.otp_totp",
        "two_factor",
    ]

# project applications
INSTALLED_APPS += ["permits"]

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

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_CONFIG_FIELDSETS = {
    "General Options": (
        "APPLICATION_TITLE",
        "APPLICATION_SUBTITLE",
        "APPLICATION_DESCRIPTION",
        "ALLOWED_FILE_EXTENSIONS",
        "MAX_FILE_UPLOAD_SIZE",
        "MAX_FEATURE_NUMBER_FOR_QGISSERVER",
        "GEOCALENDAR_URL",
        "ENABLE_GEOCALENDAR",
        "ANONYMOUS_REQUEST_SENT_TITLE",
        "ANONYMOUS_REQUEST_SENT_BODY",
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
    "ALLOWED_FILE_EXTENSIONS": (  # Supported file extensions https://pypi.org/project/filetype/
        "pdf, jpg, png",
        "Extensions autorisées lors de l'upload de document, seuls des types images PIL et PDF sont supportés",
        str,
    ),
    "MAX_FILE_UPLOAD_SIZE": (10485760, "Taille maximum des fichiers uploadés", int,),
    "MAX_FEATURE_NUMBER_FOR_QGISSERVER": (
        10,
        "Nombre maximum d'entités disponible pour QGISSERVER, un nombre trop élevé impactera négativement les performances de l'impression",
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
    "BACKGROUND_COLOR": ("#FFFFFF", "Couleur unie du fond", str,),
    "LOGIN_BACKGROUND_COLOR": ("#FFFFFF", "Couleur unie du fond login", str,),
    "PRIMARY_COLOR": ("#008c6f", "Couleur de thème principale", str,),
    "SECONDARY_COLOR": ("#01755d", "Couleur de thème secondaire", str,),
    "TEXT_COLOR": ("#000000", "Couleur du texte", str,),
    "TITLE_COLOR": ("#000000", "Couleur du titre", str,),
    "TABLE_COLOR": ("#212529", "Couleur du texte dans les tableaux", str,),
    "IP_WHITELIST": (
        "172.16.0.1,172.17.0.1,127.0.0.1,localhost",
        "IP autorisées pour l'utilisation de l'API complète (/rest/permits), séparées par des ','",
        str,
    ),
    "NETWORK_WHITELIST": (
        "172.16.0.0/12,192.168.0.0/16",
        "Réseaux autorisés pour l'utilisation de l'API complète (/rest/permits), séparés par des ','",
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
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "constance.context_processors.config",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "geomapshark.context_processors.two_factor_setting",
                "permits.context_processors.step_type",
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
    "accounts.geomapfish": {
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
    "accounts.dootix": {
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
SOCIALACCOUNT_FORMS = {"signup": "permits.forms.SocialSignupForm"}
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = None

BOOTSTRAP4 = {
    "include_jquery": True,
    # Avoid repeating the label in the placeholder
    "set_placeholder": False,
}

WSGI_APPLICATION = "geomapshark.wsgi.application"


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
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
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


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = os.environ["STATIC_URL"]
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

PRIVATE_MEDIA_ROOT = os.environ["PRIVATE_MEDIA_ROOT"]
MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")
MEDIA_ROOT = os.environ.get("MEDIA_ROOT", os.path.join(BASE_DIR, "media"))

MIN_START_DELAY = os.getenv("MIN_START_DELAY")
WMTS_GETCAP = os.getenv("WMTS_GETCAP")
WMTS_LAYER = os.getenv("WMTS_LAYER")
WMTS_GETCAP_ALTERNATIVE = os.getenv("WMTS_GETCAP_ALTERNATIVE")
WMTS_LAYER_ALTERNATIVE = os.getenv("WMTS_LAYER_ALTERNATIVE")
OL_MAP_HEIGHT = os.getenv("OL_MAP_HEIGHT")

GRAPPELLI_ADMIN_TITLE = "Interface d'administration Geocity"

# Django REST Framework
DRF_ALLOW_TOKENAUTHENTICATION = (
    os.getenv("DRF_ALLOW_TOKENAUTHENTICATION", "false").lower() == "true"
)
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "django_wfs3.pagination.CustomPagination",
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.ScopedRateThrottle",],
    "DEFAULT_THROTTLE_RATES": {
        # Full API for permits
        "permits": os.getenv("DRF_THROTTLE_RATE_PERMITS_API"),
        # Full API for permits_details
        "permits_details": os.getenv("DRF_THROTTLE_RATE_PERMITS_DETAILS_API"),
        # Limited pulic API used mainly by Geocalendar front app
        "events": os.getenv("DRF_THROTTLE_RATE_EVENTS_API"),
        # Full API for search
        "search": os.getenv("DRF_THROTTLE_RATE_SEARCH_API"),
    },
}
# Allow TokenAuthentication to the API.
if DRF_ALLOW_TOKENAUTHENTICATION:
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] += (
        "rest_framework.authentication.TokenAuthentication",
    )

WFS3_TITLE = "OGC API Features - Geocity"
WFS3_DESCRIPTION = "Point d'accès OGC API Features aux données Geocity."

CRISPY_TEMPLATE_PACK = "bootstrap4"

CRON_CLASSES = [
    "permits.cron.PermitRequestExpirationReminder",
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
