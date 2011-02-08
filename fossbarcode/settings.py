# Django settings for compliance project.

import os, time

# Function for finding the project root.

def get_project_root():
    project_root_paths = [ ".", "..", "/opt/linuxfoundation" ]
    for path in project_root_paths:
        if os.path.exists(os.path.join(path, "foss-barcode.py")) or \
                os.path.exists(os.path.join(path, "bin/foss-barcode.py")):
            return path

    # Shouldn't get here unless we can't find the path.
    raise RuntimeError, "could not find the project path"

# Return the proper directory to use for userdir mode.

def get_userdir():
    return os.path.join(os.environ["HOME"], ".fossbarcode")

# Should we use userdir mode?

def use_userdir():
    if os.getuid() == 0 or os.environ["LOGNAME"] == "compliance":
        return False
    project_root = get_project_root()
    if os.access(os.path.join(project_root, "fossbarcode"), os.W_OK):
        return False

    return True

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.

if 'TZ' not in os.environ:  # env is clear => timezone is the system one
    TIME_ZONE = 'Etc/GMT%+d' % (time.altzone / 3600)
else:                       # env is updated => timezone is obsolete
    TIME_ZONE = os.environ['TZ']

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Project root.
PROJECT_ROOT = get_project_root()

# Writable file setup; use different settings for userdir or normal mode.
if use_userdir():
    USERDIR_ROOT = get_userdir()
    DATABASE_NAME = os.path.join(USERDIR_ROOT, "barcode.sqlite")
    STATE_ROOT = USERDIR_ROOT
    USERDATA_ROOT = os.path.join(USERDIR_ROOT, "user_data")
else:
    USERDIR_ROOT = ''
    DATABASE_NAME = os.path.join(get_project_root(), 'fossbarcode', 'barcode.sqlite')
    STATE_ROOT = os.path.join(PROJECT_ROOT, 'fossbarcode')
    USERDATA_ROOT = os.path.join(PROJECT_ROOT, "fossbarcode", "user_data")

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '' 

STATIC_DOC_ROOT = os.path.join(PROJECT_ROOT, 'fossbarcode/media')
# FIXME - if we go this route (for clickable links), drop the previous defs
USERDATA_ROOT = os.path.join(PROJECT_ROOT, 'fossbarcode/media/user_data')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'wzb!69=4(kj=w)vl&lyp-j1ff9#fi8^)p^i4xr9$kokcu5j9pk'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'fossbarcode.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, "fossbarcode/templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'fossbarcode.barcode',
)
