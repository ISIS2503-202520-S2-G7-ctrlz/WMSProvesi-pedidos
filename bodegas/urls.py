from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BodegaViewSet

router = DefaultRouter()
router.register(r'bodegas', BodegaViewSet, basename='bodega')

urlpatterns = [
    path('', include(router.urls)),
]
