from django.urls import path
from . import views

app_name = 'pendientes'

urlpatterns = [
    path('jefe/', views.lista_pendientes_jefe, name='lista_jefe'),
    path('jefe/nuevo/', views.crear_pendiente, name='crear'),
    path('mios/', views.mis_pendientes, name='mis_pendientes'),
    path('<int:pk>/completar/', views.marcar_completado, name='marcar_completado'),
]
