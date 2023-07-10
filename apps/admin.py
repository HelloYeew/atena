from django.contrib import admin

from apps.models import Repository, RepositoryPermission

admin.site.register(Repository)
admin.site.register(RepositoryPermission)
