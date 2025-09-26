from django.http import JsonResponse
from .models import Pedido

def listar_pedidos(request):
    if request.method == "GET":
        pedidos = Pedido.objects.all().values()
        return JsonResponse(list(pedidos), safe=False)
