from django.urls import path
from .views import panel_home, update_configuration


urlpatterns = [
    path('', panel_home, name='panel'),
    path('update', update_configuration, name='update-configuration'),
]
