from decouple import config
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from slugify import slugify

from apis.s3 import get_s3_client
from apps.forms import RepositoryForm, RepositoryPermissionForm, RepositoryPermissionUpdateForm
from apps.models import Repository, RepositoryPermission, RepositoryAPIKey, RepositoryReleaseArtifact, RepositoryRelease
from apps.utils import generate_api_key

S3_BUCKET_NAME = config('S3_BUCKET_NAME', default='')
s3_client = get_s3_client()


@login_required
def home(request):
    permission = RepositoryPermission.objects.filter(user=request.user).order_by('-repository__updated_at')
    repository_list = []
    for permission_object in permission:
        repository_list.append(permission_object.repository)
    return render(request, 'apps/home.html', {
        'repositories': repository_list[:3]
    })


@login_required()
def repositories(request):
    permission = RepositoryPermission.objects.filter(user=request.user).order_by('-repository__updated_at')
    repository_list = []
    for permission_object in permission:
        repository_list.append(permission_object.repository)
    return render(request, 'apps/repositories/list.html', {
        'repositories': repository_list
    })


@login_required
def create_repositories(request):
    if request.method == 'POST':
        form = RepositoryForm(request.POST)
        if form.is_valid():
            repository_object = form.instance
            repository_object.created_by = request.user
            repository_object.slug = slugify(repository_object.name)
            form.save()
            RepositoryPermission.objects.create(
                repository=repository_object,
                user=request.user,
                permission='admin'
            )
            messages.success(request, f'Created repository successfully!')
            return redirect('apps_repository_detail', slug=repository_object.slug)
    else:
        form = RepositoryForm()
    return render(request, 'apps/repositories/create.html', {
        'form': form
    })


@login_required
def repository_detail(request, slug):
    repository = get_object_or_404(Repository, slug=slug)
    permission = get_object_or_404(RepositoryPermission, repository=repository, user=request.user)
    return render(request, 'apps/repositories/detail.html', {
        'repository': repository,
        'permissions': repository.permissions.all(),
        'top_menu_active': 'home',
        'total_release_count': repository.releases.count(),
        'total_pre_release_count': repository.releases.filter(pre_release=True).count(),
        'total_artifact_count': RepositoryReleaseArtifact.objects.filter(release__repository=repository).count(),
        'total_artifact_size': RepositoryReleaseArtifact.objects.filter(release__repository=repository).aggregate(
            total_size=models.Sum('size'))['total_size'] or 0,
        'latest_update': repository.updated_at,
        'permission': permission
    })


@login_required
def repository_settings_general(request, slug):
    repository = get_object_or_404(Repository, slug=slug)
    permission = get_object_or_404(RepositoryPermission, repository=repository, user=request.user)
    if not (permission.permission == 'admin' or permission.permission == 'write'):
        return render(request, '403.html', status=403)
    if request.method == 'POST':
        form = RepositoryForm(request.POST, instance=repository)
        if form.is_valid():
            form.save()
            messages.success(request, f'Updated repository successfully!')
            return redirect('apps_repository_detail', slug=repository.slug)
    else:
        form = RepositoryForm(instance=repository)
    return render(request, 'apps/repositories/settings/general.html', {
        'form': form,
        'repository': repository,
        'top_menu_active': 'settings',
        'settings_active': 'general',
        'permission': permission
    })


@login_required
def repository_releases(request, slug):
    repository = get_object_or_404(Repository, slug=slug)
    permission = get_object_or_404(RepositoryPermission, repository=repository, user=request.user)
    return render(request, 'apps/repositories/release.html', {
        'repository': repository,
        'releases': RepositoryRelease.objects.filter(repository=repository).order_by('-created_at'),
        'top_menu_active': 'release',
        'permission': permission
    })


@login_required
def repository_settings(request, slug):
    get_object_or_404(Repository, slug=slug)
    permission = get_object_or_404(RepositoryPermission, repository__slug=slug, user=request.user)
    if not (permission.permission == 'admin' or permission.permission == 'write'):
        return render(request, '403.html', status=403)
    else:
        return redirect('apps_repository_settings_general', slug=slug)


@login_required
def repository_settings_api(request, slug):
    repository = get_object_or_404(Repository, slug=slug)
    permission = get_object_or_404(RepositoryPermission, repository=repository, user=request.user)
    if not (permission.permission == 'admin' or permission.permission == 'write'):
        return render(request, '403.html', status=403)
    if RepositoryAPIKey.objects.filter(repository__slug=slug, user=request.user).exists():
        api_key = RepositoryAPIKey.objects.get(repository__slug=slug, user=request.user)
    else:
        api_key = RepositoryAPIKey.objects.create(
            repository=Repository.objects.get(slug=slug),
            key=generate_api_key(),
            user=request.user
        )
    return render(request, 'apps/repositories/settings/api.html', {
        'repository': repository,
        'api_key': api_key,
        'top_menu_active': 'settings',
        'settings_active': 'api',
        'permission': permission
    })


@login_required
def repository_settings_collaborators(request, slug):
    repository = get_object_or_404(Repository, slug=slug)
    permission = get_object_or_404(RepositoryPermission, repository=repository, user=request.user)
    if not permission.permission == 'admin':
        return render(request, '403.html', status=403)
    return render(request, 'apps/repositories/settings/collaborators.html', {
        'repository': repository,
        'top_menu_active': 'settings',
        'settings_active': 'collaborators',
        'permission': permission,
        'permission_list': RepositoryPermission.objects.filter(repository=repository)
    })


@login_required
def repository_settings_collaborators_remove(request, slug, permission_id):
    repository = get_object_or_404(Repository, slug=slug)
    permission = get_object_or_404(RepositoryPermission, repository=repository, user=request.user)
    if not permission.permission == 'admin':
        return render(request, '403.html', status=403)
    permission_object = get_object_or_404(RepositoryPermission, id=permission_id)
    # Cannot remove yourself and the owner
    if permission_object.user == request.user or permission_object.user == repository.created_by:
        messages.error(request, f'Cannot remove yourself or the owner of the repository!')
        return redirect('apps_repository_settings_collaborators', slug=slug)
    messages.success(request, f'Removed collaborator successfully!')
    return redirect('apps_repository_settings_collaborators', slug=slug)


@login_required
def repository_settings_collaborators_add(request, slug):
    repository = get_object_or_404(Repository, slug=slug)
    permission = get_object_or_404(RepositoryPermission, repository=repository, user=request.user)
    if not permission.permission == 'admin':
        return render(request, '403.html', status=403)
    if request.method == 'POST':
        form = RepositoryPermissionForm(request.POST)
        if form.is_valid():
            old_permission = RepositoryPermission.objects.filter(
                user__username=form.cleaned_data['username'],
                repository=repository
            )
            if old_permission.exists():
                form.add_error('username', 'This user already has a permission for this repository')
                return render(request, 'apps/repositories/settings/collaborators_add.html', {
                    'repository': repository,
                    'form': form,
                    'top_menu_active': 'settings',
                    'settings_active': 'collaborators',
                    'permission': permission,
                })
            RepositoryPermission.objects.create(
                user=User.objects.get(username=form.cleaned_data['username']),
                repository=repository,
                permission=form.cleaned_data['permission']
            )
            messages.success(request, f'Added collaborator successfully!')
            return redirect('apps_repository_settings_collaborators', slug=slug)
    else:
        form = RepositoryPermissionForm()
    return render(request, 'apps/repositories/settings/collaborators_add.html', {
        'repository': repository,
        'form': form,
        'top_menu_active': 'settings',
        'settings_active': 'collaborators',
        'permission': permission,
    })


@login_required
def repository_settings_collaborators_update(request, slug, permission_id):
    repository = get_object_or_404(Repository, slug=slug)
    permission = get_object_or_404(RepositoryPermission, repository=repository, user=request.user)
    if not permission.permission == 'admin':
        return render(request, '403.html', status=403)
    permission_object = get_object_or_404(RepositoryPermission, id=permission_id)
    if request.method == 'POST':
        form = RepositoryPermissionUpdateForm(request.POST, instance=permission_object)
        if form.is_valid():
            form.save()
            messages.success(request, f'Updated collaborator successfully!')
            return redirect('apps_repository_settings_collaborators', slug=slug)
    else:
        form = RepositoryPermissionUpdateForm(instance=permission_object)
    return render(request, 'apps/repositories/settings/collaborators_update.html', {
        'repository': repository,
        'form': form,
        'top_menu_active': 'settings',
        'settings_active': 'collaborators',
        'permission': permission,
        'update_permission': permission_object
    })


@login_required
def download_artifact(request, artifact_id):
    artifact = get_object_or_404(RepositoryReleaseArtifact, id=artifact_id)
    get_object_or_404(RepositoryPermission, repository=artifact.release.repository, user=request.user)
    file = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=artifact.artifact_key)
    response = HttpResponse(file['Body'].read())
    response['Content-Disposition'] = 'attachment; filename=' + artifact.get_artifact_name()
    response['Content-Type'] = file['ContentType']
    return response
