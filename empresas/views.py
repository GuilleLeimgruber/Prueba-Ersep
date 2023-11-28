from django.shortcuts import render, redirect
from .models import Actas, Empresas

def listar_actas(request):
    actas = Actas.objects.all()

    empresa_id = request.GET.get('empresa')
    interno = request.GET.get('interno')
    acta_numero = request.GET.get('acta')

    if empresa_id:
        actas = actas.filter(empresa_id=empresa_id)

    if interno:
        actas = actas.filter(interno=interno)

    if acta_numero:
        actas = actas.filter(numero_de_acta__icontains=acta_numero)

    # Obtener todas las empresas para el filtro de empresa
    empresas = Empresas.objects.all()
   
   
   
   
   
   
    return render(request, 'empresas/listar_actas.html', {'actas': actas, 'empresas': empresas})