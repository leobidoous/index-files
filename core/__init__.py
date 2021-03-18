from django.apps import AppConfig

default_app_config = 'core.CoreConfig'


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from core.routine import start
        start()
