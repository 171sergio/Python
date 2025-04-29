from django.contrib import admin
from django.urls import path, include  # <--- importa o include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # <--- adiciona essa linha
]
