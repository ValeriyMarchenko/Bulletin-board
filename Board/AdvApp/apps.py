from django.apps import AppConfig


class AdvappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AdvApp'

    def ready(self):
        import AdvApp.signals
