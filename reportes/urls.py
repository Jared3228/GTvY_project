# reportes/urls.py
from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path("", views.index_reportes, name="index"),
    path('generar/constancia/', views.generate_const, name='generar_constancia'),
    path('detalle/<int:pk>/', views.detalle_report, name='detalle'),
]
