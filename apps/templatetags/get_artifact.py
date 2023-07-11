from django import template
from django.db import models
from django.shortcuts import resolve_url

from apps.models import RepositoryRelease, RepositoryReleaseArtifact

register = template.Library()


def get_artifact(release_id: int) -> dict:
    """
    Get all artifacts from a release.
    :param release_id: The release ID.
    """
    release = RepositoryRelease.objects.get(id=release_id)
    artifact = []
    for artifact_object in RepositoryReleaseArtifact.objects.filter(release=release):
        artifact.append({
            'name': artifact_object.artifact_key.split('/')[-1],
            'size': artifact_object.size,
            'url': resolve_url('apps_download_artifact', artifact_id=artifact_object.id)
        })
    return {
        'total_artifact_count': release.artifacts.count(),
        'total_artifact_size': release.artifacts.aggregate(
            total_size=models.Sum('size')
        )['total_size'] or 0,
        'artifacts': artifact
    }


register.filter('get_artifact', get_artifact)
