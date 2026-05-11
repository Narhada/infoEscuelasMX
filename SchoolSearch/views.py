from django.shortcuts import render
from .forms import EstadoNivelForm

def seleccion_view(request):
    if request.method == "POST":
        form = EstadoNivelForm(request.POST)
        if form.is_valid():
            estado = form.cleaned_data["estado"]
            nivel = form.cleaned_data["nivel_educativo"]
            # Aquí procesas los datos (guardar, mostrar resumen, etc.)
            return render(request, "SchoolSearch/resumen.html", {"estado": estado, "nivel": nivel})
    else:
        form = EstadoNivelForm()
    return render(request, "SchoolSearch/formulario.html", {"form": form})
