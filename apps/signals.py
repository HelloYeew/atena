from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.models import RepositoryRelease, RepositoryReleaseArtifact


@receiver(post_save, sender=RepositoryRelease)
def release_post_save(sender, instance, created, **kwargs):
    instance.repository.updated_at = timezone.now()
    instance.repository.save()


@receiver(post_save, sender=RepositoryReleaseArtifact)
def artifact_post_save(sender, instance, created, **kwargs):
    instance.release.repository.updated_at = timezone.now()
    instance.release.repository.save()
