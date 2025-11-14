from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_productos, name='listar_productos'),
    path('<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
]
