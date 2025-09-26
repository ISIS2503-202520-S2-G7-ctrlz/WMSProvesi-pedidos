from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)  # identificador único
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.nombre} ({self.sku})"