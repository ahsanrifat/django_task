from django.urls import path, include
from .views import weather_of_a_city

urlpatterns = [path("city", weather_of_a_city)]
