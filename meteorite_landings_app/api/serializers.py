from rest_framework import serializers
from .models import Meteorite

class MeteoriteSerializer(serializers.ModelSerializer):
   class Meta:
      model = Meteorite
      fields = ['name', 'id', 'nametype', 'recclass', 'mass', 'fall', 'year', 'reclat', 'reclong', 'geoLocation']
