# Generated by Django 3.2.11 on 2022-03-04 13:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0026_auto_20220208_0132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genericsettings',
            old_name='verbose_name',
            new_name='display_name',
        ),
        migrations.AddField(
            model_name='genericsettings',
            name='account_number',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AlterField(
            model_name='genericsettings',
            name='custom_carrier_name',
            field=models.CharField(help_text='Unique carrier slug, lowercase alphanumeric characters and underscores only', max_length=50, validators=[django.core.validators.RegexValidator('^[a-z0-9_]+$')]),
        ),
    ]
