import re
from django.core.exceptions import ValidationError

def validar_codigo_pedido(codigo):
    """
    Valida que el código del pedido sea seguro contra SQL Injection
    """
    if not codigo:
        raise ValidationError("Código no puede estar vacío")
    
    if not re.match(r'^[A-Za-z0-9\-_]+$', codigo):
        raise ValidationError("Código contiene caracteres inválidos")
    
    # Longitud razonable
    if len(codigo) > 50:
        raise ValidationError("Código demasiado largo")
    
    return codigo

def validar_id_seguro(id_valor):
    """
    Valida que un ID sea numérico y seguro contra SQL Injection
    """
    if id_valor is None:
        raise ValidationError("ID no puede ser nulo")
    
    id_str = str(id_valor)
    
    if not re.match(r'^\d+$', id_str):
        raise ValidationError("ID debe contener solo números")
    
    id_num = int(id_str)
    if id_num <= 0:
        raise ValidationError("ID debe ser positivo")
    if id_num > 1000000:
        raise ValidationError("ID fuera de rango permitido")
    
    return id_num

def sanitizar_texto(texto):
    """
    Elimina caracteres peligrosos para SQL y XSS
    """
    if not texto:
        return ""
    
    peligrosos = ["'", '"', ';', '--', '/*', '*/', 'union', 'select', 'drop', 
                  'delete', 'insert', 'update', 'exec', 'xp_', 'script', '<', '>']
    
    sanitizado = texto
    for peligroso in peligrosos:
        sanitizado = sanitizado.replace(peligroso, '')
    
    return sanitizado.strip()