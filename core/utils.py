import uuid

def generate_short_slug():
    # Genera un UUID y toma los primeros 8 caracteres de la representación hexadecimal
    return str(uuid.uuid4().hex)[:5]