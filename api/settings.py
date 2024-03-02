"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

from api.config import Config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = Config.API.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
    "minio_storage",
    "corsheaders",
    "drf_spectacular",
    "my_user",
    "lesson",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# django-cors-headers
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://simple504api.darkube.app",
]
CORS_ORIGIN_ALLOW_ALL = True

CSRF_TRUSTED_ORIGINS = [
    "https://localhost:3000",
    "http://127.0.0.1:3000",
    "https://*.simple504api.darkube.app",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": Config.Postgres.name,
        "USER": Config.Postgres.user,
        "PASSWORD": Config.Postgres.password,
        "HOST": Config.Postgres.host,
        "PORT": Config.Postgres.port,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

ACCOUNT_EMAIL_VERIFICATION = "none" if DEBUG is True else "mandatory"
# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.environ.get("DJANGO_STATIC_ROOT")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
        #     "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    # "DEFAULT_PERMISSION_CLASSES": [
    #     "rest_framework.permissions.AllowAny"
    # ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        "rest_framework.authentication.TokenAuthentication",
        # 'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "api.standard_pagination.StandardResultsSetPagination",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Simple 504 API",
    "DESCRIPTION": "Simple 504 API Swagger UI",
    "VERSION": "0.0.1",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS
}

MEDIA_URL = "/images/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static/images")
MEDIA_PATH = "static/media"
DEFAULT_MEDIA_ROOT = os.path.join(BASE_DIR, "static/images")

DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"
STATICFILES_STORAGE = "minio_storage.storage.MinioStaticStorage"
MINIO_STORAGE_ENDPOINT = Config.Minio.end_point
MINIO_STORAGE_ACCESS_KEY = Config.Minio.access_key
MINIO_STORAGE_SECRET_KEY = Config.Minio.secret_key
MINIO_STORAGE_USE_HTTPS = Config.Minio.use_https
MINIO_STORAGE_MEDIA_BUCKET_NAME = Config.Minio.media_bucket_name
MINIO_STORAGE_STATIC_BUCKET_NAME = Config.Minio.static_bucket_name
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True
MINIO_STORAGE_MEDIA_URL = Config.Minio.media_url
MINIO_STORAGE_STATIC_URL = Config.Minio.static_url
