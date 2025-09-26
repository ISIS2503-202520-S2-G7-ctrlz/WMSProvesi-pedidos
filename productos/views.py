from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Producto

@require_GET
def listar_productos(request):
    productos = Producto.objects.all().values()
    return JsonResponse(list(productos), safe=False)
