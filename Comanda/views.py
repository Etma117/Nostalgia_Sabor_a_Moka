from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.views import View 
from .models import Carrito, CarritoItem
from Menu.models import Producto
from .forms import SeleccionSaboresForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'comanda.html')

def domicilio(request):
    return render(request, 'domicilio.html')

def salon(request):
    return render(request, 'salon.html')

class Productos(ListView):
    model = Producto
    template_name = 'Productos.html'
    context_object_name = 'Producto'

@login_required
def Carrito(request):
    carrito_id = request.session.get('carrito_id')
    carrito, created = Carrito.objects.get_or_create(id=carrito_id)

    carrito_items = carrito.carritoitem_set.all()
    total = sum(item.producto.precio * item.cantidad for item in carrito_items)

    return render(request, 'carrito.html', {'carrito_items': carrito_items, 'total': total})

@login_required
def AgregarAlCarrito(request):
    if request.method == 'POST':
        user_id = request.POST.get('user.id')
        product_id = request.POST.get('producto.id')
        quantity = int(request.POST.get('cantidad', 1))

        user = request.user
        producto = get_object_or_404(Producto, id=product_id)

        carrito_id = request.session.get('carrito_id')
        carrito, created = Carrito.objects.get_or_create(id=carrito_id)

    return redirect('view_cart')
    