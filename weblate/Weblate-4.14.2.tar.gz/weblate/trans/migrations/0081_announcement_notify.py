# Generated by Django 3.0.6 on 2020-05-28 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trans", "0080_auto_20200522_0909"),
    ]

    operations = [
        migrations.AddField(
            model_name="announcement",
            name="notify",
            field=models.BooleanField(
                blank=True, default=True, verbose_name="Notify users"
            ),
        ),
    ]
