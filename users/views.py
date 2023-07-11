from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.views import static
from django.views.decorators.http import require_GET

from users.forms import UserCreationForms, UserSettingsForm, ProfileSettingsForm


class LogoutAndRedirect(auth_views.LogoutView):
    # Redirect to / after logout
    def get_next_page(self):
        return '/'


def signup(request):
    if request.method == 'POST':
        form = UserCreationForms(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}! Now you can login.')
            return redirect('login')
    else:
        form = UserCreationForms()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def settings(request):
    return redirect('settings_profile')


@login_required
def appearance_settings(request):
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=request.user.settings)
        if form.is_valid():
            form.save()
            messages.success(request, f'Settings saved successfully!')
            return redirect('settings_appearance')
    else:
        form = UserSettingsForm(instance=request.user.settings)
    return render(request, 'users/settings/appearance.html', {'form': form})


@login_required
def profile_settings(request):
    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Settings saved successfully!')
            return redirect('settings_profile')
    else:
        form = ProfileSettingsForm(instance=request.user.profile)
    return render(request, 'users/settings/profile.html', {'form': form})


def favicon(request):
    return static.serve(request, 'favicon.ico', document_root='static')


@require_GET
def robots_txt(request):
    """
    Return the robots.txt file to tell the search engine crawlers not to index the site.
    """
    lines = [
        # Disallowed all
        "User-Agent: *",
        "Disallow: /"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
