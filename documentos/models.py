from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Documento(models.Model):
    ESTADOS = [
        ("borrador", "Borrador"),
        ("revision", "En revisión"),
        ("aprobado", "Aprobado"),
        ("rechazado", "Rechazado"),
    ]

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documentos_creados",
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default="borrador")
    marcado_para_revision = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre
