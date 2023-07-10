from django.contrib.auth.models import User
from django.db import models
from django_cryptography.fields import encrypt


class Repository(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repositories')
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-created_at']


PERMISSION = (
    ('read', 'Read'),
    ('write', 'Write'),
    ('admin', 'Admin'),
)


class RepositoryPermission(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissions')
    permission = models.CharField(max_length=20, choices=PERMISSION)

    def __str__(self):
        return f'{self.repository} - {self.user} ({self.permission})'

    class Meta:
        unique_together = ('repository', 'user')


class RepositoryAPIKey(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='api_keys')
    key = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.repository} API Key'


class RepositoryRelease(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='releases')
    version = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    pre_release = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.repository} - {self.version} ({self.created_at}, {"pre-release" if self.pre_release else "release"})'


class RepositoryReleaseArtifact(models.Model):
    release = models.ForeignKey(RepositoryRelease, on_delete=models.CASCADE, related_name='artifacts')
    artifact_key = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    size = models.BigIntegerField()

    def __str__(self):
        return f'{self.release} - {self.release.repository.name}'

    def get_artifact_key_list(self):
        return self.artifact_key.split(',')
