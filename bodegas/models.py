from django.db import models


class Bodega(models.Model):
    """
    Representa una bodega física donde se almacenan productos.
    """
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    direccion = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    capacidad_maxima = models.PositiveIntegerField(
        help_text="Capacidad máxima en unidades (o en la unidad que maneje el negocio)."
    )
    activa = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bodegas'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} ({self.codigo})'
