from django.urls import path

from .views import create_location

urlpatterns = [
    path('locations/', create_location),
]
