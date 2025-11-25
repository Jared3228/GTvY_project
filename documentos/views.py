from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt

from .models import Documento
from .forms import DocumentoForm, DocumentoRevisionForm


class DocumentoListView(LoginRequiredMixin, ListView):
    model = Documento
    template_name = 'documentos/index.html'
    context_object_name = 'documentos'
    # usamos el ordering del modelo, no hace falta más


class DocumentoCreateView(LoginRequiredMixin, CreateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'documentos/form.html'
    success_url = reverse_lazy('documentos:lista')

    def form_valid(self, form):
        documento = form.save(commit=False)
        documento.creado_por = self.request.user

        if documento.marcado_para_revision:
            documento.estado = "revision"
        else:
            documento.estado = "borrador"

        documento.save()
        return super().form_valid(form)


class DocumentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'documentos/form.html'
    success_url = reverse_lazy('documentos:lista')

    def form_valid(self, form):
        documento = form.save(commit=False)
        if documento.marcado_para_revision:
            documento.estado = "revision"
        documento.save()
        return super().form_valid(form)


class DocumentoDetailView(LoginRequiredMixin, DetailView):
    model = Documento
    template_name = 'documentos/detalle.html'
    context_object_name = 'documento'


class BandejaRevisionView(PermissionRequiredMixin, ListView):
    permission_required = 'documentos.puede_revisar_documentos'
    model = Documento
    template_name = 'documentos/bandeja_revision.html'
    context_object_name = 'documentos'

    def get_queryset(self):
        return Documento.objects.filter(marcado_para_revision=True)


class DocumentoRevisionUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'documentos.puede_revisar_documentos'
    model = Documento
    form_class = DocumentoRevisionForm
    template_name = 'documentos/revision_detalle.html'
    success_url = reverse_lazy('documentos:bandeja_revision')

    def form_valid(self, form):
        documento = form.save(commit=False)
        if documento.estado in ['aprobado', 'rechazado']:
            documento.marcado_para_revision = False
        documento.save()
        return super().form_valid(form)


@login_required
@xframe_options_exempt
def documento_pdf_view(request, pk):
    """
    Devuelve el PDF para previsualizarlo en un iframe.
    X-Frame-Options está desactivado solo aquí.
    """
    documento = get_object_or_404(Documento, pk=pk)

    if not documento.archivo:
        raise Http404("Este documento no tiene archivo asociado.")

    return FileResponse(
        documento.archivo.open('rb'),
        content_type='application/pdf'
    )
