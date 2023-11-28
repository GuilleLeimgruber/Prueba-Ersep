from django.urls import path
from .views import listar_actas

urlpatterns = [
    # ... otras URLs existentes ...
    path('listar-actas/', listar_actas, name='listar_actas'),
]