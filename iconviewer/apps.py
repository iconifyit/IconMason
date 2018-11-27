from django.apps import AppConfig

class IconViewer(AppConfig):
    name = 'iconviewer'
    verbose_name = "IconViewer"
    with open("foo.txt", mode="w") as fh:
        fh.write("je moeder")
    def ready(self):
        import iconviewer.signals
