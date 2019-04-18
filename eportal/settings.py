"""
Django settings for eportal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import email_info

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$9b^ttpvr66hxr0w6d*nep&=f5(hzdpmob)ng(a)yp*&sj1nsw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)
STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

ALLOWED_HOSTS = ['*']
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_wysiwyg',
    'django.contrib.humanize',
    'ckeditor',
    'accounts',
    'quiz',
    'student',
    'notification',
    'attendance',
)

DJANGO_WYSIWYG_FLAVOR = "ckeditor"

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
    'django.contrib.sessions.middleware.SessionMiddleware',
)

ROOT_URLCONF = 'eportal.urls'

WSGI_APPLICATION = 'eportal.wsgi.application'
OVERWRITE_EXTENDS = False

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'sqlite3.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (os.path.join(BASE_DIR, 'template'),),
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True
TRACK_PAGEVIEWS = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/uploaded_image')
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'ck')
CKEDITOR_IMAGE_BACKEND = "pillow"

EMAIL_USE_TLS = email_info.EMAIL_USE_TLS
EMAIL_HOST = email_info.EMAIL_HOST
EMAIL_HOST_USER = email_info.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = email_info.EMAIL_HOST_PASSWORD
EMAIL_PORT = email_info.EMAIL_PORT

AUTH_PROFILE_MODULE = 'student.student_profile'

GOOGLE_MAPS_KEY = 'AIzaSyCtASsXUUeOCUNgBoINuY04Hn0HuF9yuws'
TRACKING_USE_GEOIP = True
GEOIP_PATH = '/home/vc/Desktop/GeoIP.dat'
GEOIP_CACHE_TYPE = 1
DEFAULT_TRACKING_TEMPLATE = 'tracking/visitor_map.html'
ALLOWED_INCLUDE_ROOTS = ('/static/documents/html',)

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'kama',
        'toolbar': 'full',
        'height': 291,
        'width': 618,
        'filebrowserWindowWidth': 940,
        'filebrowserWindowHeight': 747,
    },
    'awesome_ckeditor': {
        'uiColor': '#14B8C4',
        'width': '700',
        'height': '400',
        'startupFocus': True,
        'margin': 0,
    },
    'admin_ckeditor': {
        'toolbar': 'full',
        'uiColor': '#14B8C4',
        'startupFocus': True,
        'margin': 0,

    },

}
