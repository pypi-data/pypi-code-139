# Generated by Django 3.0.5 on 2020-05-16 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("checks", "0003_auto_20191212_1441"),
    ]

    operations = [
        migrations.RenameField(
            model_name="check",
            old_name="ignore",
            new_name="dismissed",
        ),
    ]
