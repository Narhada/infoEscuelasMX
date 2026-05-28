from django import forms

NIVELES_EDUCATIVOS = [
    ("preescolar", "Preescolar"),
    ("primaria", "Primaria"),
    ("secundaria", "Secundaria"),
    
]

class EstadoNivelForm(forms.Form):
    numerotop = forms.IntegerField(label="Selecciona el Top", min_value=1,  max_value=32)
    #estado = forms.ChoiceField(choices=ESTADOS_MEXICO, label="Selecciona un estado")
    nivel_educativo = forms.ChoiceField(choices=NIVELES_EDUCATIVOS, label="Nivel educativo")
