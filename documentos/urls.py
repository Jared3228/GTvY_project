from django.urls import path
from .views import (
    DocumentoListView,
    DocumentoCreateView,
    DocumentoDetailView,
    DocumentoUpdateView,
    BandejaRevisionView,
    DocumentoRevisionUpdateView,
    documento_pdf_view,
)

app_name = 'documentos'

urlpatterns = [
    path('', DocumentoListView.as_view(), name='lista'),
    path('nuevo/', DocumentoCreateView.as_view(), name='crear'),
    path('<int:pk>/', DocumentoDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', DocumentoUpdateView.as_view(), name='editar'),

    # Previsualización PDF
    path('pdf/<int:pk>/', documento_pdf_view, name='pdf'),

    # Revisión jefe
    path('revision/', BandejaRevisionView.as_view(), name='bandeja_revision'),
    path('revision/<int:pk>/', DocumentoRevisionUpdateView.as_view(), name='revision_detalle'),
]