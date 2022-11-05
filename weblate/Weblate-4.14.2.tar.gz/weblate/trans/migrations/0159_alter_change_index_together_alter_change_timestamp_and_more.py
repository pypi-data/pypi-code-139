# Generated by Django 4.1 on 2022-11-04 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lang", "0017_alter_plural_type"),
        ("trans", "0158_alter_change_action"),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name="change",
            index_together=set(),
        ),
        migrations.AlterField(
            model_name="change",
            name="timestamp",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterIndexTogether(
            name="change",
            index_together={
                (
                    "timestamp",
                    "translation",
                    "project",
                    "component",
                    "language",
                    "action",
                )
            },
        ),
    ]
