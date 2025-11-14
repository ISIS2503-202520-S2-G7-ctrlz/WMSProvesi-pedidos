from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Producto
from django.shortcuts import get_object_or_404
from .validators import validar_id_seguro
from django.core.exceptions import ValidationError


@require_GET
def listar_productos(request):
    productos = Producto.objects.all().values("id", "nombre", "sku", "precio", "stock", "ubicacion")
    # opcional: convertir Decimal a float si hiciera falta
    productos_list = []
    for p in productos:
        p["precio"] = float(p["precio"])
        productos_list.append(p)
    return JsonResponse(productos_list, safe=False)


@require_GET
def detalle_producto_seguro(request, producto_id):
    """VISTA SEGURA - Protegida contra SQL Injection"""
    try:
        id_seguro = validar_id_seguro(producto_id)
        
        producto = get_object_or_404(Producto, id=id_seguro)
        
        data = {
            "id": producto.id,
            "nombre": producto.nombre,
            "sku": producto.sku,
            "precio": float(producto.precio),
            "stock": producto.stock,
            "ubicacion": producto.ubicacion or "No disponible",
            "seguro": True,  
            "mensaje": " Consulta segura - Protegida contra SQL Injection"
        }
        return JsonResponse(data)
        
    except ValidationError as e:
        return JsonResponse({
            'error': 'ID inválido detectado',
            'detalle': str(e),
            'seguro': True
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': 'Error interno del servidor',
            'seguro': True
        }, status=500)