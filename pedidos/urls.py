from django.urls import path
from . import views

urlpatterns = [
    path("pedidos/", views.listar_pedidos, name="listar_pedidos"),
    path("pedidos/<str:codigo>/", views.obtener_pedido_seguro, name="obtener_pedido_seguro"),
    path("pedidos-vulnerable/<str:codigo>/", views.obtener_pedido_vulnerable, name="obtener_pedido_vulnerable"),
]   