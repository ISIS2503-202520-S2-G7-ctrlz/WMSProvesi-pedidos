import re
from django.core.exceptions import ValidationError

def validar_id_seguro(id_valor):
    """
    Valida que un ID sea numérico y seguro contra SQL Injection
    """
    if not re.match(r'^\d+$', str(id_valor)):
        raise ValidationError("ID debe contener solo números")
    return int(id_valor)

def validar_sku_seguro(sku):
    """
    Valida que el SKU sea seguro
    """
    if not sku:
        raise ValidationError("SKU no puede estar vacío")
    
    if not re.match(r'^[A-Za-z0-9\-_]+$', sku):
        raise ValidationError("SKU contiene caracteres inválidos")
    
    if len(sku) > 50:
        raise ValidationError("SKU demasiado largo")
    
    return sku