from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate-image/', views.generate_image, name='generate-image'),
]