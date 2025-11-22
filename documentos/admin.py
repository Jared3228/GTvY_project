from django.contrib import admin

from documentos.models import Documento

# Register your models here.
@admin.register(Documento)     # esto es equivalente a admin.site.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("nombre", "descripcion")
    list_filter = ("fecha_creacion",)