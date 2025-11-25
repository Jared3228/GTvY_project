from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

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

    #  Archivo PDF
    archivo = models.FileField(
        upload_to='documentos/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        verbose_name="Archivo PDF",
    )

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
    #  Flag para que el jefe lo vea en su bandeja
    marcado_para_revision = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_creacion']
        permissions = [
            # 🔹 Esto lo usará el jefe para tener acceso a la bandeja de revisión
            ("puede_revisar_documentos", "Puede revisar y aprobar documentos"),
        ]

    def __str__(self):
        return self.nombre
