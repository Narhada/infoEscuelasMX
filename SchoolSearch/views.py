
## KASANDRA :))
from django.shortcuts import render
from .forms import EstadoNivelForm
import math
from pathlib import Path
from django.conf import settings
import psycopg2
import psycopg2.extras


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

#def seleccion_view(request):
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
def seleccion_view(request):

    if request.method == "POST":

        form = EstadoNivelForm(request.POST)

        if form.is_valid():

            mapa_niveles = {
                "preescolar": "PREESCOLAR",
                "primaria": "PRIMARIA",
                "secundaria": "SECUNDARIA",
            }

            nivel_form = form.cleaned_data.get("nivel_educativo")
            nivel_buscado = mapa_niveles.get(nivel_form)

            n = form.cleaned_data.get("numerotop")

            lat_usuario = float(request.POST.get("lat"))
            lon_usuario = float(request.POST.get("lon"))

            resultados = buscar_escuelas(
                lat_usuario,
                lon_usuario,
                nivel_buscado=nivel_buscado,
                radio_km=10
            )

            return render(
                request,
                "SchoolSearch/resumen.html",
                {
                    "escuelas": resultados[:n],
                    "lat_usuario": lat_usuario,
                    "lon_usuario": lon_usuario,
                }
            )

        # SI EL FORM NO ES VÁLIDO
        return render(
            request,
            "SchoolSearch/formulario.html",
            {
                "form": form,
                "error": "Formulario inválido"
            }
        )

    # GET
    else:
        form = EstadoNivelForm()

    return render(
        request,
        "SchoolSearch/formulario.html",
        {
            "form": form
        }
    )

import psycopg2
import psycopg2.extras

def buscar_escuelas(lat_usuario, lon_usuario, nivel_buscado=None, radio_km=10):
    conn = psycopg2.connect(
        host="127.0.0.1",
        dbname="escuelas_sep_sql",
        user="user_postgres", #   <---------------------
        password="insert_password_postgres"# <------------------
    )

    cur = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    if nivel_buscado:
        cur.execute("""
            SELECT c_nombre,
                   inmueble_c_vialidad_principal,
                   inmueble_latitud,
                   inmueble_longitud
            FROM escuelas
            WHERE inmueble_latitud IS NOT NULL
              AND inmueble_longitud IS NOT NULL
              AND UPPER(tiponivelsub_c_servicion2)=UPPER(%s)
        """, (nivel_buscado,))
    else:
        cur.execute("""
            SELECT c_nombre,
                   inmueble_c_vialidad_principal,
                   inmueble_latitud,
                   inmueble_longitud
            FROM escuelas
            WHERE inmueble_latitud IS NOT NULL
              AND inmueble_longitud IS NOT NULL
        """)

    registros = cur.fetchall()

    cur.close()
    conn.close()

    resultados = []

    for escuela in registros:

        try:
            lat = float(escuela["inmueble_latitud"])
            lon = float(escuela["inmueble_longitud"])
        except (TypeError, ValueError):
            continue

        distancia = haversine(
            lat_usuario,
            lon_usuario,
            lat,
            lon
        )

        if distancia > radio_km:
            continue

        resultados.append({
            "nombre": escuela["c_nombre"],
            "calle": escuela["inmueble_c_vialidad_principal"],
            "lat": lat,
            "lon": lon,
            "distancia": round(distancia, 2)
        })

    resultados.sort(key=lambda x: x["distancia"])

    return resultados
