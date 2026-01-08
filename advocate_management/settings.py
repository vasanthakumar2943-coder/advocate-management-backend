from pathlib import Path
from datetime import timedelta
import os
from corsheaders.defaults import default_headers

# =====================================================
# BASE
# =====================================================
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

    # third-party
    "rest_framework",
    "corsheaders",
    "channels",

    # local
    "users",
]

AUTH_USER_MODEL = "users.User"

# =====================================================
# REST FRAMEWORK (JWT)
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
# MIDDLEWARE  (ORDER IS CRITICAL)
# =====================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =====================================================
# CORS / CSRF  (VERCEL → RAILWAY)
# =====================================================



# ✅ Allow only your frontend
CORS_ALLOWED_ORIGINS = [
    "https://advocate-management-ten.vercel.app",
]

# ✅ Allow JWT headers
CORS_ALLOW_HEADERS = list(default_headers) + [
    "authorization",
]

CORS_ALLOW_CREDENTIALS = True

# ✅ CSRF (required for POST/PUT/DELETE)
CSRF_TRUSTED_ORIGINS = [
    "https://advocate-management-ten.vercel.app",
    "https://*.railway.app",
]

# =====================================================
# URLS / TEMPLATES
# =====================================================
ROOT_URLCONF = "advocate_management.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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
# STATIC & MEDIA
# =====================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


DEBUG = False

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =====================================================
# CHANNELS (STABLE – NO REDIS)
# =====================================================
ASGI_APPLICATION = "advocate_management.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

# =====================================================
# JWT SETTINGS
# =====================================================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=6),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
