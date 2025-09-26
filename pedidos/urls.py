from django.urls import path
from . import views

urlpatterns = [
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),
]
