from django.urls import path
from . import views

urlpatterns = [
    path("pedidos/", views.listar_pedidos, name="listar_pedidos"),
    path("pedidos/<str:codigo>/", views.obtener_pedido, name="obtener_pedido"),
]
