from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Convenio

from convenios.forms import ConvenioForm

from .models import Convenio

class ConvenioListView(LoginRequiredMixin, ListView):
    model = Convenio
    template_name = 'convenios/index.html'  # o como lo tengas
    context_object_name = 'convenios'

    def get_queryset(self):
        qs = Convenio.objects.all()

        # 🔹 Filtro: incluir o no deshabilitados
        show_inactive = self.request.GET.get('inactivos') == '1'
        if not show_inactive:
            qs = qs.filter(activo=True)

        # 🔹 Orden básico
        orden = self.request.GET.get('orden', 'recientes')

        if orden == 'antiguos':
            qs = qs.order_by('fecha_convenio', 'pk')
        elif orden == 'pk_asc':
            qs = qs.order_by('pk')
        elif orden == 'pk_desc':
            qs = qs.order_by('-pk')
        else:  # 'recientes' por defecto
            qs = qs.order_by('-fecha_convenio', '-pk')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orden'] = self.request.GET.get('orden', 'recientes')
        context['inactivos'] = self.request.GET.get('inactivos') == '1'
        return context

class ConvenioDetailView(LoginRequiredMixin, DetailView):
    model = Convenio
    template_name = 'convenios/detalle.html'
    context_object_name = 'convenio'

class ConvenioCreateView(LoginRequiredMixin, CreateView):
    model = Convenio
    form_class = ConvenioForm
    template_name = 'convenios/formulario.html'
    success_url = reverse_lazy('convenios:index')

    def form_valid(self, form):
        form.instance.aprobado_por = self.request.user
        return super().form_valid(form)


class ConvenioUpdateView(LoginRequiredMixin, UpdateView):
    model = Convenio
    form_class = ConvenioForm
    template_name = 'convenios/formulario.html'

    def get_success_url(self):
        return reverse_lazy('convenios:detalle', kwargs={'pk': self.object.pk})


class ConvenioToggleActivoView(LoginRequiredMixin, View):
    def post(self, request, pk):
        convenio = get_object_or_404(Convenio, pk=pk)

        # Puedes mejorar permisos aquí
        if not request.user.is_staff:
            return HttpResponseForbidden("No tienes permiso para cambiar el estado de este convenio.")

        convenio.activo = not convenio.activo
        convenio.save()

        return redirect('convenios:detalle', pk=pk)
