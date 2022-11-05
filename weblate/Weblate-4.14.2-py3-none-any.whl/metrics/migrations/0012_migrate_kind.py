# Generated by Django 3.2.6 on 2021-09-30 18:38

from django.db import migrations
from django.db.models import Case, Value, When

from weblate.metrics.models import METRIC_IDS


def migrate_kind(apps, schema_editor):
    Metric = apps.get_model("metrics", "Metric")
    db_alias = schema_editor.connection.alias
    conditions = [
        When(name=name, then=Value(kind)) for name, kind in METRIC_IDS.items()
    ]

    Metric.objects.using(db_alias).update(kind=Case(*conditions))


class Migration(migrations.Migration):

    dependencies = [
        ("metrics", "0011_metric_kind"),
    ]

    operations = [
        migrations.RunPython(
            migrate_kind, migrations.RunPython.noop, elidable=False, atomic=False
        )
    ]
