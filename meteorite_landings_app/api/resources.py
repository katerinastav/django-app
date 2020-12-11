from import_export import resources
from .models import Meteorite

class MeteoriteResource(resources.ModelResource):
    class Meta:
        model = Meteorite
