"""Deploy-time warnings so `manage.py check --deploy` catches go-live misses."""

from django.conf import settings
from django.core.checks import Error, Tags, Warning, register

from config.settings import secret_key_is_unsafe


@register(Tags.security, deploy=True)
def production_readiness(app_configs, **kwargs):
    issues = []

    if secret_key_is_unsafe(settings.SECRET_KEY):
        issues.append(
            Error(
                "DJANGO_SECRET_KEY is too weak for production (need 50+ random characters).",
                hint='python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"',
                id="pages.E001",
            )
        )

    if not settings.EMAIL_HOST:
        issues.append(
            Warning(
                "EMAIL_HOST is empty — contact-form mail is printed to the console, not delivered.",
                hint="Set EMAIL_HOST / EMAIL_HOST_USER / EMAIL_HOST_PASSWORD (and DEFAULT_FROM_EMAIL) before going live.",
                id="pages.W001",
            )
        )

    try:
        from .models import SiteSettings

        phone = SiteSettings.load().phone
    except Exception:
        phone = ""
    if "555" in (phone or ""):
        issues.append(
            Warning(
                "Public phone number still looks like the starter 555 placeholder.",
                hint="Change it under /editor/ → Site text before the site faces the internet.",
                id="pages.W002",
            )
        )

    return issues
