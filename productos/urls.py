from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.productos_list, name='listar_productos'),
    path('productos/<int:idProducto>/', views.producto_detalle, name='listar_productos'),
]
