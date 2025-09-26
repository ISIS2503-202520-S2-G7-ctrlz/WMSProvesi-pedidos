from django.contrib import admin
from .models import Pedido, DetallePedido, HistorialPedido


class DetallePedidoInline(admin.TabularInline):  # 👈 para editar productos + cantidades
    model = DetallePedido
    extra = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [DetallePedidoInline]
    list_display = ("codigo", "cliente", "estado", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("codigo", "cliente")
    list_filter = ("estado", "fecha_creacion")


@admin.register(HistorialPedido)
class HistorialPedidoAdmin(admin.ModelAdmin):
    list_display = ("pedido", "estado", "fecha", "observacion")
    list_filter = ("estado", "fecha")
