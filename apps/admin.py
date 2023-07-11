from django.contrib import admin

from apps.models import Repository, RepositoryPermission, RepositoryAPIKey, RepositoryRelease, RepositoryReleaseArtifact

admin.site.register(Repository)
admin.site.register(RepositoryPermission)
admin.site.register(RepositoryAPIKey)
admin.site.register(RepositoryRelease)
admin.site.register(RepositoryReleaseArtifact)
