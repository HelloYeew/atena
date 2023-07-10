from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from users.models import THEME_SETTINGS, Settings, Profile


class UserCreationForms(UserCreationForm):
    """Form for creating a new user."""
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserSettingsForm(forms.ModelForm):
    """Form for user settings page"""
    theme = forms.ChoiceField(
        label='Theme',
        help_text='Set the theme.',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        choices=THEME_SETTINGS
    )

    class Meta:
        model = Settings
        fields = ['theme']


class ProfileSettingsForm(forms.ModelForm):
    """Form for profile settings page"""
    avatar = forms.ImageField(
        label='Avatar',
        help_text='Set the avatar image. (This will be resized to 500x500)',
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Profile
        fields = ['avatar']
