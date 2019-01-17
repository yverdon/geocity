import os, yaml


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Load local environnement settings
#stream = open('/var/www/vhosts/yverdon-geoportail/private/gms_preprod/env.yaml','r')
stream = open(BASE_DIR + '/env.yaml','r')
customConfig = yaml.load(stream)
for k, v in customConfig['ENV_VARS'].items():
    os.environ[str(k)] = str(v)

INSTANCE_ID = os.environ["INSTANCE_ID"]

ROOT_URLCONF = 'geomapshark.urls'
LOGIN_REDIRECT_URL ='/'
#FORCE_SCRIPT_NAME = INSTANCE_ID
# LOGIN_URL = '/' + INSTANCE_ID + '/accounts/login/'
# LOGOUT_REDIRECT_URL = '/'+ INSTANCE_ID
#LOGIN_REDIRECT_URL = INSTANCE_ID + '/accounts/profile/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

YVENT_URL = os.environ["YVENT_URL"]
MAPNV_URL = os.environ["MAPNV_URL"]
SIGNALEZ_URL = os.environ["SIGNALEZ_URL"]
QGISSERVER_URL = os.environ["QGISSERVER_URL"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

os.environ["GDAL_DATA"] = os.path.join(BASE_DIR, 'gdal_data')
GDAL_DATA = os.environ["GDAL_DATA"]

ALLOWED_HOSTS = ['gmf23-mapnv.preprod.sig.cloud.camptocamp.com',
                'dev.mapnv.ch',
                'pro.mapnv.ch',
                'mapnv.ch',
                 'localhost',
                 '127.0.0.1']

DATE_INPUT_FORMAT = [
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
]

DEFAULT_FROM_EMAIL = "noreply@mapnv.ch"
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = os.environ["EMAIL_PORT"]
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_USE_TLS = os.environ["EMAIL_USE_TLS"]

DEFAULT_CHARSET = "utf-8"

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_filters',
    'bootstrap4',
    'bootstrap_datepicker_plus',
    'django_tables2',
    'fontawesome',
    'gpf'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

BOOTSTRAP4 = {
    'include_jquery': True,
}

WSGI_APPLICATION = 'geomapshark.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ["PGDATABASE"],
        'USER': os.environ["PGUSER"],
        'HOST': os.environ["PGHOST"],
        'PORT': os.environ["PGPORT"],
        'PASSWORD': os.environ["PGPASSWORD"],
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'fr-CH'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

gettext = lambda x: x

LANGUAGES = (

   ('fr', gettext('French')),

   ('en', gettext('English')),

)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
