from io import BytesIO
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.utils import timezone
from django.views.generic import ListView

from xhtml2pdf import pisa

from .forms import DatosBasicosReporteForm
from .models import Reporte

#Podria ser una buena idea, dependiendo de la dificultad y el tiempo, agregar un sistema de carga masiva
#con una plantilla de excel
#Tambien es necesario que este el atributo carrera
def render_to_pdf(template_src, context_dict=None):
    if context_dict is None:
        context_dict = {}

    template = get_template(template_src)
    html = template.render(context_dict)

    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(html.encode('UTF-8')),
        dest=result,
        encoding='UTF-8'
    )

    if pdf.err:
        return None

    return result.getvalue()


class ReporteListView(LoginRequiredMixin, ListView):
    model = Reporte
    template_name = 'reportes/index.html'
    context_object_name = 'reportes'
    # opcional: paginate_by = 20

    def get_queryset(self):
        qs = Reporte.objects.all()

        # 🔎 Búsqueda por nombre o número de control
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(nombre_alumno__icontains=q) |
                Q(numero_control__icontains=q)
            )

        # 📅 Orden
        orden = self.request.GET.get('orden', 'recientes')

        if orden == 'fecha_asc':
            qs = qs.order_by('fecha', 'pk')
        elif orden == 'fecha_desc':
            qs = qs.order_by('-fecha', '-pk')
        else:  # 'recientes' por defecto
            qs = qs.order_by('-creado_en', '-pk')

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '').strip()
        ctx['orden_actual'] = self.request.GET.get('orden', 'recientes')
        return ctx


@login_required
def detalle_reporte(request, pk):
    reporte = get_object_or_404(Reporte, pk=pk)
    return render(request, 'reportes/detalle_reporte.html', {'reporte': reporte})
    # ↑ uso tu nombre de template anterior "detalle_report.html"


@login_required
def _generar_reporte_pdf(request, tipo, template_pdf, titulo_pagina):
    """
    Vista genérica: muestra el form, genera PDF con una plantilla y
    guarda el Reporte con el archivo PDF.
    """
    if request.method == 'POST':
        form = DatosBasicosReporteForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data

            contexto_pdf = {
                'nombre_alumno': datos['nombre_alumno'],
                'numero_control': datos['numero_control'],
                'fecha': datos['fecha'],
                'fecha_hoy': timezone.now().date(),
            }

            pdf_bytes = render_to_pdf(template_pdf, contexto_pdf)

            reporte = Reporte(
                tipo=tipo,
                nombre_alumno=datos['nombre_alumno'],
                numero_control=datos['numero_control'],
                fecha=datos['fecha'],
                creado_por=request.user if request.user.is_authenticated else None,
                estado='generado',
            )

            if pdf_bytes:
                nombre_archivo = f'{tipo}_{datos["numero_control"]}_{timezone.now().strftime("%Y%m%d%H%M%S")}.pdf'
                reporte.archivo.save(nombre_archivo, ContentFile(pdf_bytes), save=False)

            reporte.save()

            return redirect('reportes:detalle', pk=reporte.pk)
    else:
        form = DatosBasicosReporteForm()

    # Puedes usar tu generate_const.html como plantilla de formulario
    return render(
        request,
        'reportes/generar_reporte.html',
        {
            'form': form,
            'titulo_pagina': titulo_pagina,
        }
    )


@login_required
def generar_constancia_residencia(request):
    return _generar_reporte_pdf(
        request,
        tipo='CONSTANCIA_RESIDENCIA',
        template_pdf='reportes/pdf_constancia_residencias.html',
        titulo_pagina='Constancia de residencias'
    )


@login_required
def generar_constancia_servicio(request):
    return _generar_reporte_pdf(
        request,
        tipo='CONSTANCIA_SERVICIO',
        template_pdf='reportes/pdf_constancia_servicio.html',
        titulo_pagina='Constancia de servicio social'
    )


@login_required
def generar_constancia_practicas(request):
    return _generar_reporte_pdf(
        request,
        tipo='CONSTANCIA_PRACTICAS',
        template_pdf='reportes/pdf_constancia_practicas.html',
        titulo_pagina='Constancia de prácticas profesionales'
    )
