# vim:fileencoding=utf-8
import os
from datetime import datetime


DEBUG = False
RUN_TESTS = True

APPEND_SLASH = False

DEBUG_PROPAGATE_EXCEPTIONS = True
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

TOX_PREFIX = os.environ.get("TOX_PREFIX", None)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": f"test",
        "USER": "docker",
        "PASSWORD": "docker",
        "HOST": "localhost",
        "PORT": "",
    }
}
SITE_ID = 1
SECRET_KEY = "1"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
ROOT_URLCONF = "test_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": True,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "constance.context_processors.config",
            ],
        },
    },
]

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "webmaster_verification",
    "test_project",
)

MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)
