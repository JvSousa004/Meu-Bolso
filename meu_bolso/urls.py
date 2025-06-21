# Meu_Bolso/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('financas/', include('financas.urls')),
    path('', include('financas.urls')),
    path('accounts/', include('django.contrib.auth.urls')), 
     path('api/', include('meu_bolso.api_urls')),
]