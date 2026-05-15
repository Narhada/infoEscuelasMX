from django.shortcuts import render
from .forms import EstadoNivelForm

def seleccion_view(request):
    if request.method == "POST":
        form = EstadoNivelForm(request.POST)
        if form.is_valid():
            return render(request, "SchoolSearch/resumen.html")
    else:
        form = EstadoNivelForm()
    return render(request, "SchoolSearch/formulario.html", {"form": form})
