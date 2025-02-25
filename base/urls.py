from django.urls import path
from . import views

app_name = 'base'  # Namespacing URLs for the app

urlpatterns = [
    path('', views.index, name='index'),  # Map index view
]
