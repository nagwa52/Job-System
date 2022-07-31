from django.apps import AppConfig


class JobSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        from . import signals
