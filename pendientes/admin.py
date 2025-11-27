from django.contrib import admin
from .models import Pendiente

@admin.register(Pendiente)
class PendienteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'asignado_por', 'asignado_a', 'completado', 'fecha_limite', 'fecha_creacion')
    list_filter = ('completado', 'asignado_a')
    search_fields = ('titulo', 'descripcion')
