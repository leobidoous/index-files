import requests
from django.apps import AppConfig

from core.routine import start


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        start()
        pass

