def sumar(a, b):
    """Devuelve la suma de dos números"""
    return a + b

def division(a, b):
    """Devuelve la división de dos números. Si b es 0, devuelve 'Error: División por cero'"""
    if b == 0:
        return 'Error: División por cero'
    return a / b
