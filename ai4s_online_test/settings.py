"""
Django settings for ai4s_online_test project.
Configured for both local Docker development and GCP production deployment.
"""
import os
from pathlib import Path
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# CORE DEPLOYMENT SETTINGS (Read from .env or environment variables)
# ==============================================================================

# SECRET_KEY is now read securely from your environment configuration.
SECRET_KEY = config('SECRET_KEY')

# DEBUG is read from the environment. CRITICAL: This must be False in production.
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS is a comma-separated string in your environment config.
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')


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
    'imagekit',
    'rest_framework',
    'storages',
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
LOGIN_REDIRECT_URL = 'core:dashboard' # Use URL names for robustness
LOGOUT_REDIRECT_URL = 'core:home'      # Use URL names

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
                'django.contrib.messages.middleware.MessageMiddleware',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ai4s_online_test.wsgi.application'

# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================
DATABASE_URL_FROM_ENV = config('DATABASE_URL', default='')
DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL_FROM_ENV,
        conn_max_age=600
    )
}
# Safety net for the Docker build process
if not DATABASES['default'].get('ENGINE'):
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}

# --- User Model ---
AUTH_USER_MODEL = 'users.CustomUser'

# --- Password Validation --- (No changes needed)
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

# --- Internationalization --- (No changes needed)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# STATIC & MEDIA FILES CONFIGURATION (Corrected and Final)
# ==============================================================================

# --- Base Static Settings (Applied in ALL environments) ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [ BASE_DIR / "static" ]
MEDIA_URL = '/media/'

# --- Environment-Specific Storage Configuration ---
GS_BUCKET_NAME = config('GS_BUCKET_NAME', default=None)

if GS_BUCKET_NAME:
    # --- Production Settings (Google Cloud Storage) ---
    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    
    # Overwrite STATIC_URL and MEDIA_URL to point to the GCS bucket.
    # The URL is constructed dynamically from the bucket name.
    STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'
    MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/media/'
    
    GS_DEFAULT_ACL = 'publicRead'
else:
    # --- Local Development Settings (Docker) ---
    # MEDIA_ROOT is only needed for local development.
    MEDIA_ROOT = BASE_DIR / 'media'

# --- Default primary key field type ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'