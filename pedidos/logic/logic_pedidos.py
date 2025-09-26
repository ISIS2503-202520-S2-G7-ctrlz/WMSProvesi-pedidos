from ..models import Pedido

def get_pedidos():
    queryset = Pedido.objects.all().order_by('-dateTime')[:10]
    return (queryset)

def create_pedido(form):
    measurement = form.save()
    measurement.save()
    return ()