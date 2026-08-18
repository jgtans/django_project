"""Django settings for seatplan project."""

import os
from pathlib import Path

from import_export.formats.base_formats import CSV

BASE_DIR = Path(__file__).resolve().parent.parent

# Секрет из переменной окружения (требование темы 7)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-dev-key-only-local")

DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

ALLOWED_HOSTS = ["*"]  # dev-режим и контейнер

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "workspaces",
    "employees",
    "debug_toolbar",
    "django_extensions",
    "pydotplus",
    "import_export",
    "django_ckeditor_5",
    # API (ДЗ 6)
    "rest_framework",
    "django_filters",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "djoser",  # ПОСЛЕ rest_framework (требование 19.pdf)
]

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
            "undo",
            "redo",
        ],
    },
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # ВЫШЕ CommonMiddleware (20.pdf)
    "django.middleware.security.SecurityMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "seatplan.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_URL = "static/"

WSGI_APPLICATION = "seatplan.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "seatplan_db"),
        "USER": os.environ.get("POSTGRES_USER", "seatplan_user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "seatplan_pass"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

INTERNAL_IPS = ["127.0.0.1"]

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "employee_list"
LOGOUT_REDIRECT_URL = "index"

IMPORT_FORMATS = [CSV]
EXPORT_FORMATS = [CSV]

# --- DRF (ДЗ 6) ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,  # пагинация по 10 (K2)
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {"AUTH_HEADER_TYPES": ("Bearer",)}  # JWT (K5)

SPECTACULAR_SETTINGS = {
    "TITLE": "SeatPlan API",
    "DESCRIPTION": "API сервиса рассадки сотрудников",
    "VERSION": "1.0.0",
}

# --- CORS (ДЗ 7, K2): открытое API, только для /api/ ---
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r"^/api/.*$"
