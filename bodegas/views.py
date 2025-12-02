from rest_framework import viewsets, filters
from .models import Bodega
from .serializers import BodegaSerializer


class BodegaViewSet(viewsets.ModelViewSet):
    """
    API CRUD para gestionar bodegas.

    Endpoints típicos (asumiendo /api/bodegas/):
    - GET    /api/bodegas/           -> lista bodegas
    - POST   /api/bodegas/           -> crea bodega
    - GET    /api/bodegas/{id}/      -> detalle
    - PUT    /api/bodegas/{id}/      -> actualiza
    - PATCH  /api/bodegas/{id}/      -> actualiza parcial
    - DELETE /api/bodegas/{id}/      -> elimina
    """
    queryset = Bodega.objects.all()
    serializer_class = BodegaSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'codigo', 'ciudad']
    ordering_fields = ['nombre', 'ciudad', 'capacidad_maxima']
    ordering = ['nombre']
