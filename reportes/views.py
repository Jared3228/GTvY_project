from django.shortcuts import render

# Create your views here.
def lista_reportes(request):
    return render(request, 'reportes/lista.html')  # crea luego ese template