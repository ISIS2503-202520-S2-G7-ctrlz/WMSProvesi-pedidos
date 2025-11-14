from ..models import Producto

def get_productos():
    queryset = Producto.objects.all()
    return (queryset)

def get_producto_by_id(id):
    queryset = Producto.objects.get(id=id)
    return (queryset)