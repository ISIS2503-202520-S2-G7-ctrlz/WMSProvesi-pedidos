from django.contrib import admin
from .models import Bodega


@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'codigo', 'ciudad', 'capacidad_maxima', 'activa')
    list_filter = ('ciudad', 'activa')
    search_fields = ('nombre', 'codigo', 'ciudad')
