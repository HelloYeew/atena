from django.urls import path

from apps import views

urlpatterns = [
    path('', views.home, name='apps_home'),
    path('repositories/', views.repositories, name='apps_repositories'),
    path('repositories/create/', views.create_repositories, name='apps_create_repositories'),
    path('repositories/<slug:slug>/', views.repository_detail, name='apps_repository_detail'),
    path('repositories/<slug:slug>/edit/', views.edit_repository, name='apps_edit_repository'),
]
