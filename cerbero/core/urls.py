from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
  
    path('health/', views.health_check, name='health-check'),
    
]