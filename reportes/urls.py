# reportes/urls.py
from django.urls import path
from .views import (
    ReporteListView,
    detalle_reporte,
    generar_constancia_practicas,
    generar_constancia_residencia,
    generar_constancia_servicio,
)

app_name = 'reportes'

urlpatterns = [
    path("", ReporteListView.as_view(), name="index"),
    path('detalle/<int:pk>/', detalle_reporte, name='detalle'),


    path('constancias/residencias/', generar_constancia_residencia, name='constancia_residencias'),
    path('constancias/servicio-social/', generar_constancia_servicio, name='constancia_servicio'),
    path('constancias/practicas/', generar_constancia_practicas, name='constancia_practicas'),
]
