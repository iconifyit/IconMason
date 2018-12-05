from django.apps import AppConfig

class IconMason(AppConfig):
    name = 'iconmason'
    verbose_name = "IconMason Backend"
    def ready(self):
        import iconmason.signals
