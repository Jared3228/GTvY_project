# reportes/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ConstanciaResidenciasForm
from .models import Reporte
from .services import generar_constancia_residencias
from django.utils import timezone

@login_required
def index_reportes(request):
    # si quieres que sólo vea los suyos: filter(creado_por=request.user)
    reportes = Reporte.objects.all().order_by('-creado_en')
    return render(request, "reportes/index.html", {
        "reportes": reportes,
    })

@login_required
def generate_const(request):
    if request.method == "POST":
        form = ConstanciaResidenciasForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data

            # 1) Generar contenido (por ahora solo HTML)
            html = generar_constancia_residencias(datos)

            # 2) Crear el registro en la BD (sin archivo aún)
            reporte = Reporte.objects.create(
                tipo='CONSTANCIA_RESIDENCIA',
                nombre_alumno=datos['nombre'],
                numero_control=datos['numero_control'],
                fecha=datos['fecha'],
                creado_por=request.user,
                estado='generado'
            )

            # 3) OPCIONAL: más adelante, aquí generas PDF, lo guardas en reporte.archivo y reporte.save()

            # 4) Mostrar detalle (previsualización) del reporte
            return redirect('reportes:detalle', pk=reporte.pk)
    else:
        form = ConstanciaResidenciasForm()

    return render(request, "reportes/generate_const.html", {
        "form": form
    })

@login_required
def detalle_report(request, pk):
    reporte = Reporte.objects.get(pk=pk)
    return render(request, "reportes/detalle_report.html", {"reporte": reporte})
