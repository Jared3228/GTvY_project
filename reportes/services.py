# reportes/services.py
from django.template.loader import render_to_string
# más adelante, aquí podrías meter librerías para PDF

def generar_constancia_residencias(datos):
    """
    datos: dict con nombre, numero_control, fecha, etc.
    Devuelve HTML. Más adelante se pasará a PDF.
    """
    html = render_to_string("reportes/plantillas/constancia_residencias.html", datos)
    return html
