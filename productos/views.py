from django.http import JsonResponse

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.views.decorators.http import require_GET

from .models import Producto
from .logic.producto_logica import get_productos, get_producto_by_id



def productos_list(request):
    productos = get_productos()
    context = {
        'product_list': productos
    }
    return render(request, 'Producto/productos.html', context)

def producto_detalle(request, idProducto):
    productos = get_producto_by_id(idProducto)
    context = {
        'product_list': [productos]
    }
    return render(request, 'Producto/productos.html', context)


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