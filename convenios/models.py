from django.conf import settings
from django.db import models
from datetime import date


class Convenio(models.Model):
    nombre = models.CharField(max_length=255)
    fecha_convenio = models.DateField()
    fecha_expiracion = models.DateField(null=True, blank=True)

    # Quién lo registró / aprobó
    aprobado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='convenios_aprobados'
    )

    contacto = models.CharField(max_length=255, blank=True)
    descripcion = models.TextField(blank=True)

    # Soft delete
    activo = models.BooleanField(default=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    expirado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.fecha_expiracion:
            self.expirado = date.today() > self.fecha_expiracion
        else:
            self.expirado = False
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        return self.nombre
