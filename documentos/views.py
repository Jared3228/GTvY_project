from django.http import JsonResponse, HttpResponseNotAllowed, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from documentos.forms import DocumentForm
from .models import Documento
from django.shortcuts import redirect, render
import json

# Create your views here.

# GET = listar documentos
# POST = crear documento (para pruebas rápidas con Postman / fetch)
@csrf_exempt
@require_http_methods(["GET", "POST"])
def documents_collection(request):
    if request.method == "GET":
        docs = list(
            Documento.objects.values(
                "id", "nombre", "descripcion", "fecha_creacion", "fecha_actualizacion"
            )
        )
        return JsonResponse({"results": docs}, safe=False)

    # POST (opcional por ahora)
    data = json.loads(request.body.decode("utf-8"))
    doc = Documento.objects.create(
        nombre=data.get("nombre", "Sin título"),
        descripcion=data.get("descripcion", ""),
    )
    return JsonResponse(
        {
            "id": doc.id,
            "nombre": doc.nombre,
            "descripcion": doc.descripcion,
            "fecha_creacion": doc.fecha_creacion,
            "fecha_actualizacion": doc.fecha_actualizacion,
        },
        status=201,
    )


# DETALLE (por si luego antigravity quiere ver/editar uno solo)
@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def document_detail(request, pk):
    try:
        doc = Documento.objects.get(pk=pk)
    except Documento.DoesNotExist:
        raise Http404("Documento no encontrado")

    if request.method == "GET":
        return JsonResponse(
            {
                "id": doc.id,
                "nombre": doc.nombre,
                "descripcion": doc.descripcion,
                "fecha_creacion": doc.fecha_creacion,
                "fecha_actualizacion": doc.fecha_actualizacion,
            }
        )

    if request.method == "PUT":
        data = json.loads(request.body.decode("utf-8"))
        doc.nombre = data.get("nombre", doc.nombre)
        doc.descripcion = data.get("descripcion", doc.descripcion)
        doc.save()
        return JsonResponse(
            {
                "id": doc.id,
                "nombre": doc.nombre,
                "descripcion": doc.descripcion,
                "fecha_creacion": doc.fecha_creacion,
                "fecha_actualizacion": doc.fecha_actualizacion,
            }
        )

    # DELETE
    doc.delete()
    return JsonResponse({"message": "Documento eliminado"})

def documents_page(request):
    documentos = Documento.objects.all()

    if request.method == "POST":
        form = DocumentForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            if request.user.is_authenticated:
                doc.creado_por = request.user
            doc.estado = "borrador"
            doc.save()
            return redirect("documentos:list")
    else:
        form = DocumentForm()

    return render(
        request,
        "documentos/list.html",
        {
            "documentos": documentos,
            "form": form,
        },
    )