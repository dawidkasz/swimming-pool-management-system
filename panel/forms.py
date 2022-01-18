from django import forms
from .models import SiteConfiguration


class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        fields = '__all__'
