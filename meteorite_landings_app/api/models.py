from django.db import models

# Create your models here.
class Meteorite(models.Model):
   name = models.CharField(max_length=50)
   id = models.BigIntegerField(primary_key=True)
   nametype = models.CharField(max_length=10, null=True, blank=True)
   recclass = models.CharField(max_length=30, null=True, blank=True)
   mass = models.FloatField(max_length=10, null=True, blank=True)
   fall = models.CharField(max_length=6, null=True, blank=True)
   year = models.BigIntegerField(null=True, blank=True)
   reclat = models.FloatField(null=True, blank=True)
   reclong = models.FloatField(null=True, blank=True)
   geoLocation = models.CharField(max_length=50, null=True, blank=True)

   def __str__(self):
      return self.name
