from django.apps import AppConfig
from django.db.models.signals import post_save


class CommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'commerce'

    def ready(self):
        import commerce.signals