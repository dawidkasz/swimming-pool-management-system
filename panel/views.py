from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from .forms import ConfigurationForm
from .utils import get_config


@require_GET
def panel_home(request):
    config = get_config()
    form = ConfigurationForm(initial=config.dict())

    return render(request, 'panel/panel.html', {'form': form})


@require_POST
def update_configuration(request):
    form = ConfigurationForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, 'Configuration has been updated.', extra_tags='success')
        return HttpResponseRedirect(reverse('panel'))

    messages.error(request, 'Form contains errors.', extra_tags='danger')
    return render(request, 'panel/panel.html', {'form': form})
