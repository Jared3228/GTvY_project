from django.db import models
from django.conf import settings

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

    def __str__(self):
        return self.titulo
