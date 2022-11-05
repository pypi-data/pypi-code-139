# Generated by Django 4.1a1 on 2022-06-29 07:18

from django.conf import settings
from django.db import migrations


def update_auditlog(apps, schema_editor):
    User = apps.get_model("weblate_auth", "User")
    AuditLog = apps.get_model("accounts", "AuditLog")
    db_alias = schema_editor.connection.alias
    logs = AuditLog.objects.using(db_alias).filter(
        user__username=settings.ANONYMOUS_USER_NAME, activity="sent-email"
    )
    for log in logs:
        try:
            log.user = User.objects.get(email=log.params["email"])
        except User.DoesNotExist:
            log.user = None
        log.save(update_fields=["user"])


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0019_alter_auditlog_user"),
    ]

    operations = [
        migrations.RunPython(update_auditlog, migrations.RunPython.noop, elidable=True),
    ]
