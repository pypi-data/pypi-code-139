# Generated by Django 2.2.9 on 2021-06-21 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPasswordHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password_1', models.CharField(blank=True, max_length=128, null=True)),
                ('password_2', models.CharField(blank=True, max_length=128, null=True)),
                ('password_3', models.CharField(blank=True, max_length=128, null=True)),
                ('password_4', models.CharField(blank=True, max_length=128, null=True)),
                ('password_5', models.CharField(blank=True, max_length=128, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
