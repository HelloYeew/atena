from django.contrib.auth.models import User
from django.db import models
from PIL import Image


THEME_SETTINGS = (
    ('', 'Atena Default'),
)


class Settings(models.Model):
    """Settings model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=20, choices=THEME_SETTINGS, default='', blank=True)

    class Meta:
        """Meta class."""
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'

    def __str__(self):
        """Return name."""
        return self.user.username + ' settings'


class Profile(models.Model):
    """Profile model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')

    class Meta:
        """Meta class."""
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        """Return name."""
        return self.user.username + ' profile'

    def save(self, *args, **kwargs):
        """Resize image on save"""
        super().save(*args, **kwargs)
        image = Image.open(self.avatar.path)
        if image.height > 500 or image.width > 500:
            output_size = (500, 500)
            image.thumbnail(output_size)
            image.save(self.avatar.path)
