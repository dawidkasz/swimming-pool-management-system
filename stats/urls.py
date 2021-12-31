from django.urls import path
from .views import stats_home


urlpatterns = [
    path('', stats_home),
]
