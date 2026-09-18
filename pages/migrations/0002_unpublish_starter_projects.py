from django.db import migrations

STARTER_SLUGS = (
    "plant-power-upgrade",
    "multi-site-rollout",
    "tenant-build-out-bas",
    "campus-fiber-backbone",
)


def unpublish_starter(apps, schema_editor):
    Project = apps.get_model("pages", "Project")
    Project.objects.filter(slug__in=STARTER_SLUGS).update(is_published=False)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(unpublish_starter, noop),
    ]
