"""
URL configuration for atena project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

from users import views as users_views

urlpatterns = [
    path('favicon.ico', users_views.favicon, name='favicon'),
    path('robots.txt', users_views.robots_txt, name='robots'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('admin/', admin.site.urls),
    path('signup/', users_views.signup, name='signup'),
    path('logout/', users_views.LogoutAndRedirect.as_view(), name='logout'),
    path('settings/', users_views.settings, name='settings'),
    path('settings/appearance', users_views.appearance_settings, name='settings_appearance'),
    path('settings/profile', users_views.profile_settings, name='settings_profile'),
    path('', include('apps.urls')),
    path('api/', include('apis.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
