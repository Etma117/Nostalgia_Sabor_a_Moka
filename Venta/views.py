from django.shortcuts import render
from .models import Venta
from datetime import datetime
from django.db.models import Sum

def Ventas(request):
    fecha = request.GET.get('fecha')
    mes = request.GET.get('mes')
    año = request.GET.get('año')
    ventas = Venta.objects.all()
    total_ventas = ventas.aggregate(Sum('total'))['total__sum'] or 0

    if fecha:
        fecha = datetime.strptime(fecha, '%Y-%m-%d')
        ventas = ventas.filter(fecha__date=fecha)

        total_ventas = ventas.aggregate(Sum('total'))['total__sum'] or 0
    if mes:
        ventas = ventas.filter(fecha__month=mes, fecha__year=año)

        total_ventas = ventas.aggregate(Sum('total'))['total__sum'] or 0

    return render(request, 'venta.html', {'ventas': ventas, 'years': range(2024, 2034 ), 'total_ventas':total_ventas})
