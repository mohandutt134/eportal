"""
Django settings for smvdu_portal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from .email_info import *
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$9b^ttpvr66hxr0w6d*nep&=f5(hzdpmob)ng(a)yp*&sj1nsw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quiz',
    'student',
    'django_extensions',
    'django.contrib.admindocs',
    'accounts',
    'south',
    'notification',
    'smartextends',
    'attendance',
    'django.contrib.humanize',
)


FAKER_LOCALE = None     # settings.LANGUAGE_CODE is loaded
FAKER_PROVIDERS = None

# Minimum password strength settings. See the GitHub page for defaults.
# https://github.com/dstufft/django-passwords/
SITE_ID = 1
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'online_status.middleware.OnlineStatusMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
)
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'template'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
ROOT_URLCONF = 'smvdu_portal.urls'

WSGI_APPLICATION = 'smvdu_portal.wsgi.application'
OVERWRITE_EXTENDS = False

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'sqlite3.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
    
)
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True
TRACK_PAGEVIEWS = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/uploaded_image')
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)



EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT


AUTH_PROFILE_MODULE='student.student_profile'



GOOGLE_MAPS_KEY='AIzaSyCtASsXUUeOCUNgBoINuY04Hn0HuF9yuws'
TRACKING_USE_GEOIP=True
GEOIP_PATH = '/home/vc/Desktop/GeoIP.dat'
GEOIP_CACHE_TYPE = 1
DEFAULT_TRACKING_TEMPLATE='tracking/visitor_map.html'