from django.apps import AppConfig

class IconMason(AppConfig):
    name = 'backend'
    verbose_name = "IconMason Backend"
    def ready(self):
        import backend.signals
