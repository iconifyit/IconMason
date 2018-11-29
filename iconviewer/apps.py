from django.apps import AppConfig

class IconViewer(AppConfig):
    name = 'iconviewer'
    verbose_name = "IconViewer"
    def ready(self):
        import iconviewer.signals
