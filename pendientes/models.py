from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Pendiente(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)

    asignado_por = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pendientes_creados'
    )
    asignado_a = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pendientes_asignados'
    )

    completado = models.BooleanField(default=False)
    fecha_limite = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def esta_atrasado(self):
        return True

        hoy = timezone.localdate()
        # Atrasado si ya pasó la fecha límite y no está completado
        return (not self.completado) and (self.fecha_limite < hoy)
