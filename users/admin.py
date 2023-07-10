from django.contrib import admin

from users.models import Settings, Profile

admin.site.register(Settings)
admin.site.register(Profile)
