# reportes/models.py
from django.conf import settings
from django.db import models

class Reporte(models.Model):
    TIPO_CHOICES = [
        ('CONSTANCIA_RESIDENCIA', 'Constancia de residencias'),
        # luego agregas más...
    ]

    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    nombre_alumno = models.CharField(max_length=150)
    numero_control = models.CharField(max_length=20)
    fecha = models.DateField()

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='reportes_creados'
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    # Para el flujo futuro de revisión
    ESTADO_CHOICES = [
        ('generado', 'Generado'),
        ('en_revision', 'En revisión'),
        ('aprobado', 'Aprobado'),
    ]
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='generado'
    )

    # Archivo generado (PDF/Word/lo que sea). No lo guardes como BLOB en la DB,
    # usa FileField para guardar en /media y solo guardar la ruta.
    archivo = models.FileField(
        upload_to='reportes/',
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.nombre_alumno}"
