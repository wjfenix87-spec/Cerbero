from django.urls import path
from . import views

urlpatterns = [
    path('api/upload-folder/', views.upload_folder, name='upload-folder'),
]