from django.urls import path
from .views import tickets_home


urlpatterns = [
    path('', tickets_home, name='home'),
]
