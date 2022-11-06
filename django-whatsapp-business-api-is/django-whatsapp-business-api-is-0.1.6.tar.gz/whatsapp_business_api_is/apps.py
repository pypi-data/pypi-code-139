import logging
from inspect import getmembers

from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string


class WhatsappBusinessApiIsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'whatsapp_business_api_is'
    ACTIONS = {}
    VALIDATORS = {}

    def ready(self):
        from .tasks import parse_incoming_message
        settings.INCOMING_PARSER = parse_incoming_message

        for app in settings.INSTALLED_APPS:

            try:
                module = import_string(f"{app}.bot_validators")

                for name, func in getmembers(module.Validators):
                    if name.startswith('_'):
                        continue
                    self.VALIDATORS[f"{app}.{name}"] = func
            except ImportError:
                pass

            try:
                module = import_string(f"{app}.bot_functions")

                for name, func in getmembers(module.Functions):
                    if name.startswith('_'):
                        continue
                    if name in self.ACTIONS:
                        raise ValueError(f"duplicate key '{name}' found")
                    self.ACTIONS[name] = func
            except ImportError:
                pass

        logging.debug("\n\n[actions]\n  . " + '\n  . '.join(self.ACTIONS.keys()))
        logging.debug("\n\n[validators]\n  . " + '\n  . '.join(self.VALIDATORS.keys()))
