from django.contrib import admin
from .models import Reporte

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo", "nombre_alumno", "numero_control", "fecha", "estado", "creado_en")
    search_fields = ("nombre_alumno", "numero_control")
    list_filter = ("tipo", "estado")
