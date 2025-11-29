from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q  # 👈 IMPORTANTE

from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt

from .models import Documento
from .forms import DocumentoForm, DocumentoRevisionForm

#Agregar una opcion para el rol Jefe para cambiar estado
class DocumentoListView(LoginRequiredMixin, ListView):
    model = Documento
    template_name = 'documentos/index.html'
    context_object_name = 'documentos'
    paginate_by = 20  # opcional, pero queda más "pro"

    def get_queryset(self):
        qs = Documento.objects.all()

        # 🔎 Búsqueda por nombre del archivo o nombre del creador
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q) |
                Q(creado_por__username__icontains=q) |
                Q(creado_por__first_name__icontains=q) |
                Q(creado_por__last_name__icontains=q)
            )

        # 📌 Orden: recientes (default), fecha asc, fecha desc
        orden = self.request.GET.get('orden', 'recientes')

        if orden == 'fecha_asc':
            qs = qs.order_by('fecha_creacion')
        elif orden == 'fecha_desc':
            qs = qs.order_by('-fecha_creacion')
        else:
            # "recientes" → usamos el ordering por defecto del modelo
            qs = qs.order_by('-fecha_creacion')

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['orden_actual'] = self.request.GET.get('orden', 'recientes')
        ctx['query_actual'] = self.request.GET.get('q', '').strip()
        return ctx


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
