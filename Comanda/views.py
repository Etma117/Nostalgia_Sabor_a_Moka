<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> e4e796027b5578c93ccdb4fcc368d9ec7b9c18d9
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.views import View 
from .models import Carrito, CarritoItem
<<<<<<< HEAD
from Menu.models import Producto
from .forms import SeleccionSaboresForm
from django.contrib.auth.decorators import login_required
=======
=======
<<<<<<< HEAD
from django.shortcuts import render, redirect
=======
from django.shortcuts import render
>>>>>>> 8cfbabb16bc1dc01662fb6a3e2298a4aec853728
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Carrito
>>>>>>> 0ccc6d3432fb769f9660fe04cfb10d994629baf9
from Menu.models import Producto
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
>>>>>>> e4e796027b5578c93ccdb4fcc368d9ec7b9c18d9

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

<<<<<<< HEAD
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
    
=======
<<<<<<< HEAD
@login_required
def mostrar_carrito(request):
    carrito = Carrito.objects.get_or_create(usuario=request.user)[0]
    items_carrito = carrito.carritoitem_set.all()
    
    for item in items_carrito:
        item.subtotal = item.producto.precio * item.cantidad
=======
    def get(self, request, producto_id):
        producto = Producto.objects.get(pk=producto_id)
        carrito, created = Carrito.objects.get_or_create(usuario=request.user, producto=producto)
        carrito.cantidad += 1
        carrito.save()
<<<<<<< HEAD
        return redirect('carrito')
=======
        return redirect('carrito')
>>>>>>> 0ccc6d3432fb769f9660fe04cfb10d994629baf9

    total = sum(item.subtotal for item in items_carrito)

<<<<<<< HEAD
    return render(request, 'carrito.html', {'items_carrito': items_carrito, 'total' : total })

@login_required
def añadir_producto_al_carrito(request):
    if request.method == 'POST':
        user_id = request.POST.get('id_cliente')
        product_id = request.POST.get('id_producto')
        cantidad = int(request.POST.get('cantidad', 1))

        user = get_object_or_404(User, id=user_id)
        product = get_object_or_404(Producto, id=product_id)

        sabores_seleccionados = request.POST.getlist('sabores')
        carrito, created = Carrito.objects.get_or_create(usuario=user)
    
        for sabor in sabores_seleccionados:
            carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=product, sabor=sabor)

            if carrito_item:
                carrito_item.cantidad += cantidad
                carrito_item.save()
            else:
                # Si el CarritoItem no existe, créalo
                carrito = Carrito.objects.get_or_create(usuario=user)[0]
                CarritoItem.objects.create(carrito=carrito, producto=product, cantidad=cantidad, sabor=sabor)

      
    return redirect('Productos')

@login_required
def eliminar_producto_del_carrito(request, carrito_item_id):
    carrito_item = get_object_or_404(CarritoItem, id=carrito_item_id)
    
    if carrito_item.carrito.usuario == request.user:
        carrito_item.delete()

    return redirect('mostrar_carrito')
=======
    def get(self, request):
        carrito_items = Carrito.objects.filter(usuario=request.user)
        return render(request, 'carrito.html', {'carrito_items': carrito_items})
>>>>>>> 8cfbabb16bc1dc01662fb6a3e2298a4aec853728
>>>>>>> 0ccc6d3432fb769f9660fe04cfb10d994629baf9
>>>>>>> e4e796027b5578c93ccdb4fcc368d9ec7b9c18d9
