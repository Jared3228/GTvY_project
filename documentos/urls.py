# documentos/urls.py
from django.urls import path
from . import views

app_name = 'documentos'

urlpatterns = [
    # Vista html
    path('', views.documents_page, name='list'),

     # API
    path("api/", views.documents_collection, name="api_list"),
    path("api/<int:pk>/", views.document_detail, name="api_detail"),
]
