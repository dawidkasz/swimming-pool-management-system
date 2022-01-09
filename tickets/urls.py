from django.urls import path
from .views import tickets_home, make_reservation


urlpatterns = [
    path('', tickets_home, name='home'),
    path('/reservation', make_reservation, name='make-reservation')
]
