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
    key = encrypt(models.CharField(max_length=32, unique=True))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.repository} API Key'
