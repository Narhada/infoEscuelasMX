from django.urls import path

from . import views

urlpatterns = [
    path("", views.seleccion_view, name="seleccion"),
]
