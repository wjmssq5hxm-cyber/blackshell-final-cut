import os

from django.core.exceptions import ImproperlyConfigured
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

from django.conf import settings
from config.settings import secret_key_is_unsafe

if not settings.DEBUG and secret_key_is_unsafe(settings.SECRET_KEY):
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY must be a unique 50+ character value when DEBUG is off. "
        "Generate one with: python -c \"from django.core.management.utils import "
        "get_random_secret_key; print(get_random_secret_key())\""
    )
