from django.urls import path
from . import views

urlpatterns = [
    path('listar/', views.listar_pedidos, name='listar_pedidos'),
    path('<str:codigo>/', views.obtener_pedido, name='obtener_pedido'),
]
