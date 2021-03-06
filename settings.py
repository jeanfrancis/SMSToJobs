# Django settings for txt2wrk project.

import sys
import os.path
import posixpath

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

sys.path.append(PROJECT_ROOT + '/apps')
sys.path.append(PROJECT_ROOT + '/third-party')
sys.path.append(PROJECT_ROOT + '/third-party/apps')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.sqlite3',
        'NAME' : 'dev.db',
    }
}

AUTH_PROFILE_MODULE = 'account.Profile'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'US/Pacific'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = 'public/media/'
STATIC_MEDIA_PATH = 'public/media/'
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5540gcktvmcx#_738+k#diemz$a-jh@&j6h4i=p&e8r3z1r+rr'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'txt2wrk.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    'registration',
    'tabs',
    'prelaunch',
    'common',
    'account',
    'applicant',
    'south',
    'sms',
    'job',
    'job_recommendation',
    'employer',
    'call',
)

AUTHENTICATION_BACKENDS = (
    'account.backends.ApplicantModelBackend',    
    'django.contrib.auth.backends.ModelBackend',
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'common.helpers.demo_mode',
)

# Static files
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    ('images', 'media/images'),
    ('css', 'media/css'),
    ('js', 'media/js'),
)

# Twilio REST API version
API_VERSION = '2010-04-01'

# Twilio AccountSid and AuthToken
ACCOUNT_SID = 'PUT_YOUR_TWILIO_ACCOUNT_SID_HERE_OR_IN_LOCAL_SETTINGS'
ACCOUNT_TOKEN = 'PUT_YOUR_TWILIO_AUTH_TOKEN_HERE_OR_IN_LOCAL_SETTINGS'

# Outgoing Caller ID previously validated with Twilio
CALLER_ID = 'PUT_YOUR_TXT_CALLBACK_NUMBER_HERE_OR_IN_LOCAL_SETTINGS';

APPLICANT_HOST = 'PUT_YOUR_JOB_SEEKER_DOMAIN_HERE_OR_IN_LOCAL_SETTINGS'
EMPLOYER_HOST = 'PUT_YOUR_EMPLOYER_DOMAIN_HERE_OR_IN_LOCAL_SETTINGS'

# email settings.
EMAIL_USE_TLS = True
EMAIL_HOST = 'PUT_YOUR_EMAIL_HOST_HERE_OR_IN_LOCAL_SETTINGS'
EMAIL_HOST_USER = 'PUT_YOUR_EMAIL_USERNAME_HERE_OR_IN_LOCAL_SETTINGS'
EMAIL_HOST_PASSWORD ='PUT_YOUR_EMAIL_PASSWORD_HERE_OR_IN_LOCAL_SETTINGS'
EMAIL_PORT = 587

DEMO_ENABLED = False

ACCOUNT_ACTIVATION_DAYS = 1

def local_overrides(global_dict):
    pass

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
    local_overrides(globals())
except ImportError:
    pass

