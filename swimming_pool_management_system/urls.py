from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('stats/', include('stats.urls'), name='stats'),
    path('panel/', include('panel.urls'), name='panel'),
    path('', include('tickets.urls')),
]
