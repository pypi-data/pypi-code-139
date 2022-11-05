# Generated by Django 3.1.7 on 2021-03-30 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("metrics", "0003_fixup_non_unique"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="metric",
            unique_together={("date", "scope", "relation", "name")},
        ),
        migrations.AlterIndexTogether(
            name="metric",
            index_together=set(),
        ),
    ]
