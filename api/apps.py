from django.apps import AppConfig
from ai.core import Core

# (this is not working for the moment)
# from .models import Gallery 

class ApiConfig(AppConfig):
    name = 'api'
    # core = Core()

    def ready(self):
        pass
        # feats = Gallery.objects.values_list('features',flat=True)
        # core.load_gallery_feats(feats)
