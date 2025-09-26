from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Pedido

def listar_pedidos(request):
    if request.method == "GET":
        pedidos_data = []
        pedidos = Pedido.objects.all()

        for pedido in pedidos:
            # productos con cantidad
            productos_data = [
                {
                    "producto": detalle.producto.nombre,
                    "cantidad": detalle.cantidad,
                }
                for detalle in pedido.detallepedido_set.all()
            ]

            # historial del pedido
            historial_data = [
                {
                    "estado": h.get_estado_display(),
                    "fecha": h.fecha.strftime("%Y-%m-%d %H:%M"),
                    "observacion": h.observacion,
                }
                for h in pedido.historial.all().order_by("fecha")
            ]

            # datos principales del pedido
            pedido_data = {
                "codigo": pedido.codigo,
                "cliente": pedido.cliente,
                "estado": pedido.get_estado_display(),
                "fecha_creacion": pedido.fecha_creacion.strftime("%Y-%m-%d %H:%M"),
                "fecha_actualizacion": pedido.fecha_actualizacion.strftime("%Y-%m-%d %H:%M"),
                "detalles": pedido.detalles,
                "productos": productos_data,
                "historial": historial_data,
            }

            pedidos_data.append(pedido_data)

        return JsonResponse(pedidos_data, safe=False)


def obtener_pedido(request, codigo):
    if request.method == "GET":
        pedido = get_object_or_404(Pedido, codigo=codigo)

        # productos con cantidad
        productos_data = [
            {
                "producto": detalle.producto.nombre,
                "cantidad": detalle.cantidad,
            }
            for detalle in pedido.detallepedido_set.all()
        ]

        # historial del pedido
        historial_data = [
            {
                "estado": h.get_estado_display(),
                "fecha": h.fecha.strftime("%Y-%m-%d %H:%M"),
                "observacion": h.observacion,
            }
            for h in pedido.historial.all().order_by("fecha")
        ]

        # datos principales
        pedido_data = {
            "codigo": pedido.codigo,
            "cliente": pedido.cliente,
            "estado": pedido.get_estado_display(),
            "fecha_creacion": pedido.fecha_creacion.strftime("%Y-%m-%d %H:%M"),
            "fecha_actualizacion": pedido.fecha_actualizacion.strftime("%Y-%m-%d %H:%M"),
            "detalles": pedido.detalles,
            "productos": productos_data,
            "historial": historial_data,
        }

        return JsonResponse(pedido_data, safe=False)