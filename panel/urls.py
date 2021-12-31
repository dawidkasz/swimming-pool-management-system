from django.urls import path
from .views import panel_home


urlpatterns = [
    path('', panel_home, name='panel'),
]
