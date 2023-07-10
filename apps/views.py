from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from slugify import slugify

from apps.forms import RepositoryForm
from apps.models import Repository, RepositoryPermission, RepositoryAPIKey
from apps.utils import generate_api_key


def home(request):
    return render(request, 'apps/home.html')


@login_required()
def repositories(request):
    return render(request, 'apps/repositories/list.html', {
        'repositories': Repository.objects.filter(created_by=request.user).order_by('-updated_at')
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
    repository = Repository.objects.get(slug=slug)
    return render(request, 'apps/repositories/detail.html', {
        'repository': repository,
        'permissions': repository.permissions.all(),
        'top_menu_active': 'home'
    })


@login_required
def repository_settings_general(request, slug):
    repository = Repository.objects.get(slug=slug)
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
        'settings_active': 'general'
    })


@login_required
def repository_settings(request, slug):
    return redirect('apps_repository_settings_general', slug=slug)


@login_required
def repository_settings_api(request, slug):
    if RepositoryAPIKey.objects.filter(repository__slug=slug).exists():
        api_key = RepositoryAPIKey.objects.get(repository__slug=slug)
    else:
        api_key = RepositoryAPIKey.objects.create(
            repository=Repository.objects.get(slug=slug),
            key=generate_api_key()
        )
    return render(request, 'apps/repositories/settings/api.html', {
        'repository': Repository.objects.get(slug=slug),
        'api_key': api_key,
        'top_menu_active': 'settings',
        'settings_active': 'api'
    })
