from django.conf import settings
from django.urls import path

from apis import views

urlpatterns = [
    path('upload_artifact', views.UploadArtifact.as_view(), name='api_upload_artifact')
]

if settings.DEBUG:
    urlpatterns += [
        path('upload', views.UploadFile.as_view(), name='api_upload')
    ]
