from django.urls import path

from apps import views

urlpatterns = [
    path('', views.home, name='apps_home'),
    path('repositories/', views.repositories, name='apps_repositories'),
    path('repositories/create/', views.create_repositories, name='apps_create_repositories'),
    path('repositories/<slug:slug>/', views.repository_detail, name='apps_repository_detail'),
    path('repositories/<slug:slug>/releases/', views.repository_releases, name='apps_repository_releases'),
    path('repositories/<slug:slug>/settings/', views.repository_settings, name='apps_repository_settings'),
    path('repositories/<slug:slug>/settings/general', views.repository_settings_general, name='apps_repository_settings_general'),
    path('repositories/<slug:slug>/settings/api', views.repository_settings_api, name='apps_repository_settings_api'),
    path('repositories/<slug:slug>/settings/collaborators', views.repository_settings_collaborators, name='apps_repository_settings_collaborators'),
    path('repositories/<slug:slug>/settings/collaborators/add', views.repository_settings_collaborators_add, name='apps_repository_settings_collaborators_add'),
    path('repositories/<slug:slug>/settings/collaborators/remove/<int:permission_id>', views.repository_settings_collaborators_remove, name='apps_repository_settings_collaborators_remove'),
    path('repositories/<slug:slug>/settings/collaborators/<int:permission_id>', views.repository_settings_collaborators_update, name='apps_repository_settings_collaborators_update'),
    path('artifacts/<int:artifact_id>', views.download_artifact, name='apps_download_artifact')
]
