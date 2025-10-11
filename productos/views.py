from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Producto
from django.shortcuts import get_object_or_404


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
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    data = {
        "id": producto.id,
        "nombre": producto.nombre,
        "sku": producto.sku,
        "precio": float(producto.precio),
        "stock": producto.stock,
        "ubicacion": producto.ubicacion or "No disponible"
    }
    return JsonResponse(data)