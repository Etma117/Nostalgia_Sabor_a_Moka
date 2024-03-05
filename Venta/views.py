from datetime import timezone
from django.shortcuts import render
from django.views.generic import ListView
from .models import Carrito, Venta

class ventas(ListView):
    model = Venta
    template_name = 'venta.html'
    context_object_name = 'Venta'
 

def Pagar(request):
    if request.method == 'POST':
        carrito_id = request.POST.get('carrito_id')
        carrito = Carrito.objects.get(id=carrito_id)

        items_carrito = carrito.carritoitem_set.all()

        for item in items_carrito:
            item.subtotal = item.producto.precio * item.cantidad

        total = sum(item.subtotal for item in items_carrito)
        venta = Venta(carrito=carrito)
        venta.save()

    return render(request, 'ventas', {'total':total})
