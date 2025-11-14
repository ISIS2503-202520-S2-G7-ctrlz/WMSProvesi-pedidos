from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/<int:producto_id>/', views.detalle_producto_seguro, name='detalle_producto_seguro'),
    path('productos-vulnerable/<str:producto_id>/', views.detalle_producto, name='detalle_producto_vulnerable'),
]