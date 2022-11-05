# Generated by Django 3.1.1 on 2020-10-02 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trans", "0104_update_source_unit_source"),
        ("screenshots", "0003_fill_translation"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="screenshot",
            name="component",
        ),
        migrations.AlterField(
            model_name="screenshot",
            name="translation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="trans.translation"
            ),
        ),
    ]
