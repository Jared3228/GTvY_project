from django.urls import path
from .views import (
    ConvenioListView,
    ConvenioDetailView,
    ConvenioCreateView,
    ConvenioUpdateView,
    ConvenioToggleActivoView,
)

app_name = 'convenios'

urlpatterns = [
    path('', ConvenioListView.as_view(), name='index'),
    path('nuevo/', ConvenioCreateView.as_view(), name='crear'),
    path('<int:pk>/', ConvenioDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', ConvenioUpdateView.as_view(), name='editar'),
    path('<int:pk>/toggle-activo/', ConvenioToggleActivoView.as_view(), name='toggle_activo'),
]
