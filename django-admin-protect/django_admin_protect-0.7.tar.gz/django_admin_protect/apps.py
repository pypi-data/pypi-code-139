from django.apps import AppConfig

import importlib


class DjangoAdminProtectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_admin_protect'

    DEFAULT_SETTINGS = {
        "TEMPLATE_TITLE": "Django Admin",
        "UPDATE_ADMIN_PATH": {
            "INCLUDING": False,
            "EVERY": 60 * 60 * 2
        },
        "OTP": {
            "DATE_ISSUED": 60 * 15,
            "GENERATOR": None,
            "WIDTH": 6,
            "MESSAGE_TITLE": "OTP",
            "MESSAGE_BODY": "OTP: %s",
            "MAIL_FIELDS": ["email"]
        }
    }
    SETTINGS = DEFAULT_SETTINGS.copy()

    def ready(self):
        super().ready()

        from django.conf import settings
        from . import urls 

        urlconf = importlib.import_module(settings.ROOT_URLCONF)

        for url in urls.urlpattents:
            urlconf.urlpatterns.insert(0, url)

        if hasattr(settings, "DJANGO_ADMIN_PROTECT"):
            self.update_settings(DjangoAdminProtectConfig.SETTINGS, settings.DJANGO_ADMIN_PROTECT)

        if (DjangoAdminProtectConfig.SETTINGS.get("UPDATE_ADMIN_PATH", {}).get("INCLUDING") or \
            DjangoAdminProtectConfig.DEFAULT_SETTINGS["UPDATE_ADMIN_PATH"]["INCLUDING"]):
            ...

    def update_settings(self, default_settings, settings):
        for key, value in default_settings.items():
            if new_value := settings.get(key):
                if isinstance(value, dict):
                    if isinstance(new_value, dict):
                        self.update_settings(value, new_value)
                else:
                    default_settings[key] = new_value
