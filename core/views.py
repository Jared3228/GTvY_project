from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from pendientes.models import Pendiente
from documentos.models import Documento
@login_required
def dashboard(request):
    user = request.user

    mis_pendientes = Pendiente.objects.filter(
        asignado_a=user,
        completado=False
    ).order_by('fecha_limite', 'fecha_creacion')[:5]

    # Contador de documentos marcados para revisión
    # (el template decide si mostrarlo solo al Jefe con el filtro es_jefe)
    documentos_en_revision_count = Documento.objects.filter(
        marcado_para_revision=True
    ).count()

    return render(request, 'core/dashboard.html', {
        'mis_pendientes': mis_pendientes,
        'documentos_en_revision_count': documentos_en_revision_count,
    })
