# Development settings

from .base import *

SECRET_KEY = "wdik08q)1+q%e(+v^3@g+^@n2(v^1mn=koabc-u9w%#8r%^)ej"

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "SocialDjango",
        "USER": "kamil",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
