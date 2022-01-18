from django.shortcuts import render
from .forms import ConfigurationForm


def panel_home(request):
    form = ConfigurationForm()

    return render(request, 'panel/panel.html', {'form': form})
