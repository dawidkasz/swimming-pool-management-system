from django.urls import path
from .views import tickets_home, make_reservation, reservation_pay, generate_qr


urlpatterns = [
    path('', tickets_home, name='home'),
    path('reservation/', make_reservation, name='make-reservation'),
    path('pay/', reservation_pay, name='pay-for-reservation'),
    path('qr/<str:id>/', generate_qr, name='generate-qr')
]
