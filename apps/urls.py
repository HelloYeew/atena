from django.urls import path

from apps import views

urlpatterns = [
    path('', views.home, name='apps_home'),
    path('repositories/', views.repositories, name='apps_projects'),
]
