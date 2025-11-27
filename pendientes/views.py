# pendientes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden

from .models import Pendiente
from .forms import PendienteForm
from .utils import es_jefe
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
@user_passes_test(es_jefe)
def lista_pendientes_jefe(request):
    """
    Jefe: ve todos los pendientes que él creó.
    """
    pendientes = Pendiente.objects.filter(
        asignado_por=request.user
    ).order_by('completado', 'fecha_limite')

    return render(request, 'pendientes/lista_jefe.html', {
        'pendientes': pendientes,
    })


@login_required
@user_passes_test(es_jefe)
def crear_pendiente(request):
    """
    Jefe: crea un pendiente y lo asigna a:
    - un usuario específico (asignado_a), o
    - todos los usuarios de un rol (grupo)
    """
    if request.method == 'POST':
        form = PendienteForm(request.POST)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            descripcion = form.cleaned_data['descripcion']
            fecha_limite = form.cleaned_data['fecha_limite']
            asignado_a = form.cleaned_data.get('asignado_a')
            grupo = form.cleaned_data.get('grupo')

            # Si seleccionó un rol/grupo
            if grupo:
                usuarios = User.objects.filter(groups=grupo)

                if not usuarios.exists():
                    # Si ese rol no tiene usuarios, regresamos el form con error
                    form.add_error('grupo', 'Ese rol no tiene usuarios asignados.')
                else:
                    for usuario in usuarios:
                        Pendiente.objects.create(
                            titulo=titulo,
                            descripcion=descripcion,
                            asignado_por=request.user,
                            asignado_a=usuario,
                            fecha_limite=fecha_limite,
                        )
                    return redirect('pendientes:lista_jefe')

            # Si NO hay grupo, pero sí usuario individual
            if asignado_a and not grupo:
                pendiente = Pendiente(
                    titulo=titulo,
                    descripcion=descripcion,
                    asignado_por=request.user,
                    asignado_a=asignado_a,
                    fecha_limite=fecha_limite,
                )
                pendiente.save()
                return redirect('pendientes:lista_jefe')
    else:
        form = PendienteForm()

    return render(request, 'pendientes/crear.html', {
        'form': form,
    })


@login_required
def mis_pendientes(request):
    """
    Cualquier usuario: ve SOLO sus pendientes.
    """
    pendientes = Pendiente.objects.filter(
        asignado_a=request.user,
        completado=False
    ).order_by('fecha_limite', 'fecha_creacion')

    return render(request, 'pendientes/mis_pendientes.html', {
        'pendientes': pendientes,
    })


@login_required
def marcar_completado(request, pk):
    """
    Marca un pendiente como completado si:
    - el usuario es el asignado
    - o el usuario es jefe y lo creó
    """
    pendiente = get_object_or_404(Pendiente, pk=pk)

    puede_modificar = (
        pendiente.asignado_a == request.user
        or (es_jefe(request.user) and pendiente.asignado_por == request.user)
    )

    if not puede_modificar:
        return HttpResponseForbidden("No tienes permiso para modificar este pendiente.")

    pendiente.completado = True
    pendiente.save()

    if es_jefe(request.user):
        return redirect('pendientes:lista_jefe')
    else:
        return redirect('pendientes:mis_pendientes')
