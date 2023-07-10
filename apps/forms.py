from django import forms

from apps.models import Repository


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
