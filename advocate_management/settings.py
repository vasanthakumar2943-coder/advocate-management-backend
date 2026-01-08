from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================================
# SECURITY
# =====================================================
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

DEBUG = False

ALLOWED_HOSTS = [
    "web-production-d827.up.railway.app",
    ".railway.app",
    "localhost",
    "127.0.0.1",
]

# =====================================================
# APPS
# =====================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # third party
    "rest_framework",
    "corsheaders",

    # local
    "users",
]

AUTH_USER_MODEL = "users.User"

# =====================================================
# MIDDLEWARE  (⚠️ ORDER VERY IMPORTANT)
# =====================================================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # MUST BE FIRST
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

# =====================================================
# CORS / CSRF  (VERCEL → RAILWAY)
# =====================================================
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "https://advocate-management-ten.vercel.app",
]

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "accept",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CSRF_TRUSTED_ORIGINS = [
    "https://advocate-management-ten.vercel.app",
    "https://*.railway.app",
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# =====================================================
# REST FRAMEWORK
# =====================================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# =====================================================
# URLS / TEMPLATES
# =====================================================
ROOT_URLCONF = "advocate_management.urls"

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

# =====================================================
# DATABASE
# =====================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

# =====================================================
# I18N
# =====================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# =====================================================
# STATIC / MEDIA
# =====================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =====================================================
# CACHE (typing indicator safe)
# =====================================================
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# =====================================================
# JWT
# =====================================================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=6),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}
