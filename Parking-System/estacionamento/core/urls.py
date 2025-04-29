from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),         # página principal
    path('home/', views.home, name='home'),       # lista de carros
    path('entrada/', views.entrada, name='entrada'),  # form de entrada
    path('saida/<int:carro_id>/', views.saida, name='saida'),  # saída
    path('dashboard/', views.dashboard, name='dashboard'),     # estatísticas
]
