from django import forms
from django.contrib.auth.models import User

from apps.models import Repository, RepositoryPermission


class RepositoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='The name of the repository.'
    )
    url = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control'}),
        help_text='The URL of the repository.'
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        help_text='The description of the repository.',
        required=False
    )

    class Meta:
        model = Repository
        fields = ('name', 'url', 'description')


class RepositoryPermissionForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='The username of the collaborator.'
    )
    permission = forms.ChoiceField(
        choices=(
            ('read', 'Read'),
            ('write', 'Write'),
            ('admin', 'Admin'),
        ),
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='The permission to give to the collaborator.'
    )

    def validate_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('The username does not exist.')
        return username

    # validate data
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if username:
            if not User.objects.filter(username=username).exists():
                self.add_error('username', 'The username does not exist.')
        return cleaned_data


class RepositoryPermissionUpdateForm(forms.ModelForm):
    permission = forms.ChoiceField(
        choices=(
            ('read', 'Read'),
            ('write', 'Write'),
            ('admin', 'Admin'),
        ),
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='The permission to give to the collaborator.'
    )

    class Meta:
        model = RepositoryPermission
        fields = ('permission',)
