import importlib

from django.apps import AppConfig, apps
from .settings import RECOMMENDS_AUTODISCOVER_MODULE


class RecommendsConfig(AppConfig):
    name = 'recommends'

    def ready(self):
        if not RECOMMENDS_AUTODISCOVER_MODULE:
            return

        for appconfig in apps.get_app_configs():
            try:
                importlib.import_module('.' + RECOMMENDS_AUTODISCOVER_MODULE, appconfig.name)
            except ImportError:
                pass
