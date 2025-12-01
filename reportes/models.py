# reportes/models.py
from django.conf import settings
from django.db import models

CARRERA_CHOICES = [
    ('ING_BIOQUIMICA', 'Ingeniería Bioquímica'),
    ('ING_SEMICONDUCTORES', 'Ingeniería en Semiconductores'),
    ('CONTADOR_PUBLICO', 'Contador Público'),
    ('ING_ADMINISTRACION', 'Ingeniería en Administración'),
    ('ING_DESARROLLO_APLICACIONES', 'Ingeniería en Desarrollo de Aplicaciones'),
    ('ING_ELECTRICA', 'Ingeniería Eléctrica'),
    ('ING_ELECTRONICA', 'Ingeniería Electrónica'),
    ('ING_ENERGIAS_RENOVABLES', 'Ingeniería en Energías Renovables'),
    ('ING_GESTION_EMPRESARIAL', 'Ingeniería en Gestión Empresarial'),
    ('ING_INDUSTRIAL', 'Ingeniería Industrial'),
    ('ING_LOGISTICA', 'Ingeniería en Logística'),
    ('ING_MATERIALES', 'Ingeniería en Materiales'),
    ('ING_MECATRONICA', 'Ingeniería Mecatrónica'),
    ('ING_MECANICA', 'Ingeniería Mecánica'),
    ('ING_QUIMICA', 'Ingeniería Química'),
    ('ING_SISTEMAS_COMPUTACIONALES', 'Ingeniería en Sistemas Computacionales'),
]
class Reporte(models.Model):
    TIPO_CHOICES = [
        ('CONST_RES', 'Constancia de Residencias'),
        ('CONST_SERV', 'Constancia de Servicio Social'),
        ('CONST_PRA', 'Constancia de Prácticas Profesionales'),
    ]
    
    carrera = models.CharField(
        max_length=60,
        choices=CARRERA_CHOICES,
    )
    
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    nombre_alumno = models.CharField(max_length=150)
    numero_control = models.CharField(max_length=20)
    fecha = models.DateField()
    creado_en = models.DateTimeField(auto_now_add=True)

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='reportes_creados'
    )
    #Falta agregar la opcion para que el rol Jefe pueda revisar y cambiar el estado.
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

    # Archivo generado (PDF/Word/lo que sea).
    # Se usa FileField para guardar en /media y solo guardar la ruta.
    archivo = models.FileField(
        upload_to='reportes/',
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.nombre_alumno}"
