from django.urls import include, path
from . import views

urlpatterns = [
  path('welcome', views.welcome),
  path('getmeteorites', views.get_meteorites),
  path('addmeteorite', views.add_meteorite),
  path('updatemeteorite/<int:meteorite_id>', views.update_meteorite),
  path('deletemeteorite/<int:meteorite_id>', views.delete_meteorite)
]
