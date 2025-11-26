from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import hashlib

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

    hash_archivo = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        editable=False,
        unique=True  # opcional
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

    def _calcular_hash(self):
        """
        Calcula el hash SHA256 del archivo actual SIN cerrar el archivo
        y dejando el puntero donde estaba.
        """
        archivo = self.archivo

        if not archivo:
            return None

        sha = hashlib.sha256()

        # Guardamos la posición actual del puntero
        try:
            pos_inicial = archivo.tell()
        except (AttributeError, OSError, ValueError):
            pos_inicial = None

        # Si es un UploadedFile, usamos chunks()
        if hasattr(archivo, 'chunks'):
            for chunk in archivo.chunks():
                sha.update(chunk)
        else:
            # fallback por si es otro tipo de file
            contenido = archivo.read()
            sha.update(contenido)

        # Regresar el puntero donde estaba (o al inicio)
        try:
            if pos_inicial is not None:
                archivo.seek(pos_inicial)
            else:
                archivo.seek(0)
        except (AttributeError, OSError, ValueError):
            # si no soporta seek, lo ignoramos
            pass

        return sha.hexdigest()

    def clean(self):
        """
        Validación de modelo: evita que se suba dos veces exactamente el mismo archivo.
        """
        super().clean()

        if self.archivo:
            nuevo_hash = self._calcular_hash()

            if nuevo_hash:
                qs = Documento.objects.filter(hash_archivo=nuevo_hash)
                if self.pk:
                    qs = qs.exclude(pk=self.pk)

                if qs.exists():
                    raise ValidationError({
                        'archivo': 'Ya existe un documento con este mismo archivo (contenido idéntico).'
                    })

                self.hash_archivo = nuevo_hash

    def save(self, *args, **kwargs):
        # Ya calculamos hash_archivo en clean(), aquí no tocamos el archivo
        super().save(*args, **kwargs)