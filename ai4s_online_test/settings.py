"""
Django settings for ai4s_online_test project.
Configured for local development and PythonAnywhere deployment.
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# CORE SETTINGS (with local development defaults)
# These values will be overridden by local_settings.py in production.
# ==============================================================================

# This is a safe, non-secret key for DEVELOPMENT ONLY.
# The REAL production key MUST be in your local_settings.py file on the server.
SECRET_KEY = "django-insecure-zh9n64om@@*e9qui7gpyq_%el^lkob0w3zllq@jbc40l!dm!-a"

# DEBUG is True for local development to see detailed error pages.
# It MUST be set to False in local_settings.py for production.
DEBUG = True

# For local development, this can be empty or ['127.0.0.1', 'localhost'].
# It MUST be set to your domain in local_settings.py for production.
ALLOWED_HOSTS = []


# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'imagekit',
    'rest_framework',
    # 'storages', # Not needed for PythonAnywhere's local file storage

    # Your apps
    'core',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ai4s_online_test.urls'

# --- User Authentication URLs ---
LOGIN_URL = 'users:login_register'
LOGIN_REDIRECT_URL = 'core:dashboard'
LOGOUT_REDIRECT_URL = 'core:home'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / "templates" ],
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

WSGI_APPLICATION = 'ai4s_online_test.wsgi.application'


# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================
# By default, we will use a simple SQLite database for local development.
# The local_settings.py file will override this with the MySQL configuration for production.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# --- User Model ---
AUTH_USER_MODEL = 'users.CustomUser'

# --- Password Validation ---
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

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# STATIC & MEDIA FILES CONFIGURATION (for PythonAnywhere)
# ==============================================================================
# URL to use when referring to static files.
STATIC_URL = '/static/'
# The directory where `collectstatic` will gather all static files from all apps.
STATIC_ROOT = BASE_DIR / 'staticfiles'
# We do not need STATICFILES_DIRS if all static files are inside their respective apps.

# URL that handles user-uploaded media files.
MEDIA_URL = '/media/'
# The directory where user-uploaded media files will be stored.
MEDIA_ROOT = BASE_DIR / 'media'


# --- Default primary key field type ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================================
# LOCAL SETTINGS OVERRIDE (CRITICAL FOR PRODUCTION)
# ==============================================================================
# This will try to import all settings from a local_settings.py file.
# This file should exist ONLY on the production server (PythonAnywhere) and
# should be in your .gitignore file.
try:
    from .local_settings import *
except ImportError:
    pass