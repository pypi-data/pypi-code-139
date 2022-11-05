# Generated by Django 3.2.10 on 2022-01-24 19:16

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import re


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0022_carrier_metadata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genericsettings',
            old_name='name',
            new_name='verbose_name',
        ),
        migrations.AddField(
            model_name='genericsettings',
            name='custom_carrier_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=50, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')]),
            preserve_default=False,
        ),
    ]
