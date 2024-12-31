import os
from pathlib import Path
import platform

# Set GDAL library path dynamically
if platform.system() == 'Windows':
    GDAL_LIBRARY_PATH = r"C:\Users\cecil\miniconda3\envs\awm_env\Library\bin\gdal.dll"
else:
    GDAL_LIBRARY_PATH = '/opt/conda/envs/awm_env/lib/libgdal.so'
os.environ['GDAL_LIBRARY_PATH'] = GDAL_LIBRARY_PATH

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent
# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Your app's static directory
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Directory where collectstatic will gather all static files



# Whitenoise configuration for serving static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-secret-key')
DEBUG = True  # Change to False in production
ALLOWED_HOSTS = ['localhost', '127.0.0.1','13.48.100.18','heritagesites.xyz','www.heritagesites.xyz']  # Modify for production (e.g., ['yourdomain.com'])

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'heritage_sites',
    'leaflet',
    'pwa', 
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL configuration
ROOT_URLCONF = 'assignment1.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# WSGI application
WSGI_APPLICATION = 'assignment1.wsgi.application'

# Database
# Database configuration
# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',  # PostGIS database engine
        'NAME': 'heritage_db',  # Your PostGIS database name
        'HOST': 'localhost',  # Container name for your PostgreSQL/PostGIS database
        'USER': 'c21379843',  # Database user
        'PASSWORD': 'cece123',  # Database password
        'PORT': '',  # Port for PostgreSQL
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Leaflet configuration
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (53.0, -8.0),
    'DEFAULT_ZOOM': 6,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
    'RESET_VIEW': False,
    'SCALE': None,
    'OPACITY': 0.5,
}
# PWA specific settings
PWA_APP_NAME = 'Heritage Sites Locator'
PWA_APP_DESCRIPTION = "Explore heritage sites near you"
PWA_APP_THEME_COLOR = '#000000'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_START_URL = '/'
PWA_APP_ICONS = [
    {
        'src': '/static/images/icons/icon-72x72.png',
        'sizes': '72x72',
        'type': 'image/png',
    },
    {
        'src': '/static/images/icons/icon-96x96.png',
        'sizes': '96x96',
        'type': 'image/png',
    },
    {
        'src': '/static/images/icons/icon-144x144.png',
        'sizes': '144x144',
        'type': 'image/png',
    },
    {
        'src': '/static/images/icons/icon-192x192.png',
        'sizes': '192x192',
        'type': 'image/png',
    },
    {
        'src': '/static/images/icons/icon-512x512.png',
        'sizes': '512x512',
        'type': 'image/png',
    },
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/images/icons/icon-152x152.png',
        'sizes': '152x152',
        'type': 'image/png',
    },
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/splash-640x1136.png',
        'sizes': '640x1136',
        'type': 'image/png',
    },
    {
        'src': '/static/images/splash-750x1334.png',
        'sizes': '750x1334',
        'type': 'image/png',
    },
    {
        'src': '/static/images/splash-1242x2208.png',
        'sizes': '1242x2208',
        'type': 'image/png',
    },
    {
        'src': '/static/images/splash-1125x2436.png',
        'sizes': '1125x2436',
        'type': 'image/png',
    },
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'

