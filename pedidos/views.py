from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Pedido
from .validators import validar_codigo_pedido
from django.core.exceptions import ValidationError


def listar_pedidos(request):
    if request.method == "GET":
        pedidos_data = []
        pedidos = Pedido.objects.all()

        for pedido in pedidos:
            productos_data = [
                {
                    "producto": detalle.producto.nombre,
                    "cantidad": detalle.cantidad,
                    "ubicacion": detalle.producto.ubicacion,
                }
                for detalle in pedido.detallepedido_set.all()
            ]

            historial_data = [
                {
                    "estado": h.get_estado_display(),
                    "fecha": h.fecha.strftime("%Y-%m-%d %H:%M"),
                    "observacion": h.observacion,
                }
                for h in pedido.historial.all().order_by("fecha")
            ]
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


def obtener_pedido_seguro(request, codigo):
    """
    VISTA SEGURA - Protegida contra SQL Injection
    """
    if request.method == "GET":
        try:
            codigo_seguro = validar_codigo_pedido(codigo)
            
            pedido = get_object_or_404(Pedido, codigo=codigo_seguro)
            
            productos_data = [
                {
                    "producto": detalle.producto.nombre,
                    "cantidad": detalle.cantidad,
                    "ubicacion": detalle.producto.ubicacion,
                }
                for detalle in pedido.detallepedido_set.all()
            ]

            historial_data = [
                {
                    "estado": h.get_estado_display(),
                    "fecha": h.fecha.strftime("%Y-%m-%d %H:%M"),
                    "observacion": h.observacion,
                }
                for h in pedido.historial.all().order_by("fecha")
            ]

            pedido_data = {
                "codigo": pedido.codigo,
                "cliente": pedido.cliente,
                "estado": pedido.get_estado_display(),
                "fecha_creacion": pedido.fecha_creacion.strftime("%Y-%m-%d %H:%M"),
                "fecha_actualizacion": pedido.fecha_actualizacion.strftime("%Y-%m-%d %H:%M"),
                "detalles": pedido.detalles,
                "productos": productos_data,
                "historial": historial_data,
                "seguro": True,  
                "mensaje": "Consulta segura - Protegida contra SQL Injection"
            }

            return JsonResponse(pedido_data, safe=False)
            
        except ValidationError as e:
            return JsonResponse({
                'error': 'Código inválido detectado',
                'detalle': str(e),
                'seguro': True
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': 'Error interno del servidor',
                'seguro': True
            }, status=500)


def obtener_pedido_vulnerable(request, codigo):
    """
    VISTA VULNERABLE - NO USAR EN PRODUCCIÓN
    Solo para demostración
    """
    if request.method == "GET":
        pedido = get_object_or_404(Pedido, codigo=codigo)
        
        productos_data = [
            {
                "producto": detalle.producto.nombre,
                "cantidad": detalle.cantidad,
                "ubicacion": detalle.producto.ubicacion,
            }
            for detalle in pedido.detallepedido_set.all()
        ]

        historial_data = [
            {
                "estado": h.get_estado_display(),
                "fecha": h.fecha.strftime("%Y-%m-%d %H:%M"),
                "observacion": h.observacion,
            }
            for h in pedido.historial.all().order_by("fecha")
        ]

        pedido_data = {
            "codigo": pedido.codigo,
            "cliente": pedido.cliente,
            "estado": pedido.get_estado_display(),
            "fecha_creacion": pedido.fecha_creacion.strftime("%Y-%m-%d %H:%M"),
            "fecha_actualizacion": pedido.fecha_actualizacion.strftime("%Y-%m-%d %H:%M"),
            "detalles": pedido.detalles,
            "productos": productos_data,
            "historial": historial_data,
            "vulnerable": True, 
            "advertencia": "ESTA VISTA ES VULNERABLE A SQL INJECTION"
        }

        return JsonResponse(pedido_data, safe=False)