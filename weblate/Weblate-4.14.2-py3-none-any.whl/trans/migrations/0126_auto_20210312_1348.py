# Generated by Django 3.1.7 on 2021-03-12 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("trans", "0125_unit_details"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="component",
            name="committer_email",
        ),
        migrations.RemoveField(
            model_name="component",
            name="committer_name",
        ),
    ]
