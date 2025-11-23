from django.contrib import admin
from .models import Convenio


@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_convenio', 'fecha_expiracion', 'aprobado_por', 'activo', 'expirado')
    list_filter = ('activo', 'fecha_convenio', 'fecha_expiracion', 'expirado')
    search_fields = ('nombre', 'contacto', 'descripcion')