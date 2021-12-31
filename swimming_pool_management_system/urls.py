from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('stats/', include('stats.urls')),
    path('panel/', include('panel.urls')),
    path('', include('tickets.urls')),
]
