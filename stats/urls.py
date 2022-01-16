from django.urls import path
from .views import stats_home, income_data, paid_unpaid_reservations_data


urlpatterns = [
    path('', stats_home, name='stats'),
    path('income/', income_data, name='income-data'),
    path('reservations/', paid_unpaid_reservations_data, name='reservations-data')
]
