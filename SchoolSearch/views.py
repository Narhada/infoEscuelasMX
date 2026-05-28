from django.shortcuts import render
from .forms import EstadoNivelForm
import json
import math
from pathlib import Path
from django.conf import settings

#calcula la ditsnacia sobre la esfera terrestre
# lat1 y lon1 ubi del usuario --- lat2 y lon2 ubi escuela
def haversine(lat1, lon1, lat2, lon2):

    R=6371 #radio de la tierra
    dlat=math.radians(lat2-lat1)
    dlon=math.radians(lon2-lon1)

    a =(
        math.sin(dlat/2) **2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon/2) **2
    )

    c=2*math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R*c
#regreso la distancia en km

def seleccion_view(request):
    if request.method == "POST":
        form = EstadoNivelForm(request.POST)

        #valido que este bien
        if form.is_valid(): 

            mapa_niveles = {
                "preescolar": "PREESCOLAR",
                "primaria": "PRIMARIA",
                "secundaria": "SECUNDARIA",
                
            }

            nivel_form = form.cleaned_data.get("nivel_educativo")
            
            nivel_buscado = mapa_niveles.get(nivel_form)
            n = form.cleaned_data.get("numerotop")

            #ubi usario
            lat_usuario = float(request.POST.get("lat"))
            lon_usuario = float(request.POST.get("lon"))

            ruta = Path(settings.BASE_DIR) / "data" / "escuelas_mexico.json"


            #abro el archivo 
            with open(ruta, encoding="utf-8") as f:
                escuelas = json.load(f)

            resultados = []

            for escuela in escuelas:

                nivel_escuela = (
                    escuela.get("TIPONIVELSUB_C_SERVICION2")
                    or ""
                ).strip().upper()

                if nivel_buscado and nivel_escuela.upper() != nivel_buscado:
                    continue

                lat = escuela.get("INMUEBLE_LATITUD")
                lon = escuela.get("INMUEBLE_LONGITUD")
                #si no son validas las cordenadas salto esa escuela
                if not lat or not lon:
                    continue

                try:

                    lat= float(lat)
                    lon =float(lon)

                    nivel_form = form.cleaned_data.get("nivel_educativo")
                    nivel_escuela = (escuela.get("TIPONIVELSUB_C_SERVICION2") or "")

                    if nivel_form and nivel_form.upper() != nivel_escuela.upper():
                        continue

                    distancia = haversine(
                        lat_usuario,
                        lon_usuario,
                        lat,
                        lon
                    )

                    resultados.append({
                        "nombre": escuela.get("C_NOMBRE"),
                        "lat": lat,
                        "lon": lon,
                        "distancia": round(distancia, 2)
                    })
                #la ignoro si algo sale raro
                except:
                    continue

            resultados.sort(key=lambda x: x["distancia"])#ordeno

            return render(
                request,
                "SchoolSearch/resumen.html",
                {
                    "escuelas": resultados[:n],
		    "lat_usuario": lat_usuario,
		    "lon_usuario": lon_usuario,

                }
            )

    else:
        form=EstadoNivelForm() #formulario vacio
    return render(
        request,
        "SchoolSearch/formulario.html",
        {
            "form":form
        }
    )