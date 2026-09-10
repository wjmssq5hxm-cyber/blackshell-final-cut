from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pages"
    verbose_name = "Website content"

    def ready(self):
        from django.db.backends.signals import connection_created

        from . import checks  # noqa: F401

        connection_created.connect(_sqlite_pragma)


def _sqlite_pragma(sender, connection, **kwargs):
    if connection.vendor != "sqlite":
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA busy_timeout=5000;")
            cursor.execute("PRAGMA foreign_keys=ON;")
    except Exception:
        pass
