from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.listar_pedidos, name='listar_productos'),
]
