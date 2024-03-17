from django.shortcuts import render
from .models import VentaItem, Venta

def Ventas(request):
    ventas = Venta.objects.all()
    ventaitem = VentaItem.objects.all()

    return render(request, 'venta.html', {'ventas':ventas, 'ventaitem':ventaitem})
