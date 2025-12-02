from rest_framework import serializers
from .models import Bodega


class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodega
        fields = [
            'id',
            'nombre',
            'codigo',
            'direccion',
            'ciudad',
            'capacidad_maxima',
            'activa',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
