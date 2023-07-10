from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.models import Repository


def home(request):
    return render(request, 'apps/home.html')


@login_required()
def repositories(request):
    return render(request, 'apps/repositories.html', {
        'repositories': Repository.objects.filter(created_by=request.user).order_by('-updated_at')
    })
