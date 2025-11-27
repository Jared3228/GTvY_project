from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from pendientes.models import Pendiente

@login_required
def dashboard(request):
    user = request.user

    mis_pendientes = Pendiente.objects.filter(
        asignado_a=user,
        completado=False
    ).order_by('fecha_limite', 'fecha_creacion')[:5]

    return render(request, 'core/dashboard.html', {
        'mis_pendientes': mis_pendientes,
    })
