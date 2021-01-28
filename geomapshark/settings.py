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

CLEAR_PUBLIC_SCHEMA_ON_FIXTURIZE = os.getenv("CLEAR_PUBLIC_SCHEMA_ON_FIXTURIZE")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

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

# 2FA activation
ENABLE_2FA = os.getenv("ENABLE_2FA", "false").lower() == "true"

# Application definition
INSTALLED_APPS = [
    "grappelli",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "constance",
    "constance.backends.database",
    "simple_history",
    "corsheaders",
    "django_filters",
    "rest_framework",
    "rest_framework_gis",
    "bootstrap4",
    "bootstrap_datepicker_plus",
    "django_tables2",
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
]

if ENABLE_2FA:
    MIDDLEWARE += ["django_otp.middleware.OTPMiddleware"]

MIDDLEWARE += [
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
        "MAX_FILE_UPLOAD_SIZE",
        "GEOCALENDAR_URL",
    ),
    "Theme Options": (
        "BACKGROUND_COLOR",
        "PRIMARY_COLOR",
        "SECONDARY_COLOR",
        "TEXT_COLOR",
        "TITLE_COLOR",
        "TABLE_COLOR",
    ),
    "Step Options": (
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
}

CONSTANCE_CONFIG = {
    "APPLICATION_TITLE": (
        "Demandes d'autorisations touchant le territoire communal",
        "Titre de la page de login",
        str,
    ),
    "APPLICATION_SUBTITLE": (
        "Petits travaux, abattages, fouilles, dépôts,...",
        "Sous-titre de la page de login",
        str,
    ),
    "APPLICATION_DESCRIPTION": (
        "Une application du Système d'Information du Territoire de la Ville d'Yverdon-les-Bains - mapnv.ch",
        "Description de la page de login",
        str,
    ),
    "MAX_FILE_UPLOAD_SIZE": (
        10485760,
        "Taille maximum des fichiers uploadé, penser à modifier également APPENDICES_STEP pour informer l'utilisateur de la taille maximale autorisée",
        int,
    ),
    "GEOCALENDAR_URL": (
        "https://geocity.mapnv.ch/geocalendar",
        "URL de l'application calendrier cartographique",
        str,
    ),
    "LOCATION_STEP": ("Sélectionnez la commune / l'entité", "", str),
    "WORKS_TYPES_STEP": (
        "Sélectionnez le ou les type(s) de travaux / événement(s) prévu(s)",
        "",
        str,
    ),
    "WORKS_OBJECTS_STEP": ("Sélectionnez les objets", "", str),
    "PROPERTIES_STEP": ("Renseignez les caractéristiques des objets", "", str),
    "GEO_TIME_STEP": ("Renseignez le planning et la localisation", "", str),
    "TIME_STEP": ("Renseignez le planning", "", str),
    "GEO_STEP": ("Renseignez la localisation", "", str),
    "APPENDICES_STEP": ("Ajouter des documents", "", str),
    "ACTORS_STEP": ("Renseignez les contacts", "", str),
    "SUBMIT_STEP": ("Résumé et envoi", "", str),
    "APPLICATION_TITLE": (
        "Demandes d'autorisations touchant le territoire communal",
        "Titre de la page de login",
        str,
    ),
    "APPLICATION_SUBTITLE": (
        "Petits travaux, abattages, fouilles, dépôts,...",
        "Sous-titre de la page de login",
        str,
    ),
    "APPLICATION_DESCRIPTION": (
        "Une application du Système d'Information du Territoire de la Ville d'Yverdon-les-Bains - mapnv.ch",
        "Description de la page de login",
        str,
    ),
    "BACKGROUND_COLOR": ("#FFFFFF", "Couleur unie du fond", str,),
    "PRIMARY_COLOR": ("#008c6f", "Couleur de theme principale", str,),
    "SECONDARY_COLOR": ("#01755d", "Couleur de theme secondaire", str,),
    "TEXT_COLOR": ("#000000", "Couleur du texte", str,),
    "TITLE_COLOR": ("#000000", "Couleur du titre", str,),
    "TABLE_COLOR": ("#212529", "Couleur du texte dans les tableaux", str,),
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


if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

# Internationalization

LANGUAGE_CODE = "fr-CH"
TIME_ZONE = "CET"
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

PRINTED_REPORT_LAYERS = os.getenv("PRINTED_REPORT_LAYERS")
MIN_START_DELAY = os.getenv("MIN_START_DELAY")
WMTS_GETCAP = os.getenv("WMTS_GETCAP")
WMTS_LAYER = os.getenv("WMTS_LAYER")
WMTS_GETCAP_ALTERNATIVE = os.getenv("WMTS_GETCAP_ALTERNATIVE")
WMTS_LAYER_ALTERNATIVE = os.getenv("WMTS_LAYER_ALTERNATIVE")
OL_MAP_HEIGHT = os.getenv("OL_MAP_HEIGHT")

GRAPPELLI_ADMIN_TITLE = "Interface d'administration Geocity"
