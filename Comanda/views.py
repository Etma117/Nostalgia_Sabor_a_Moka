from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Carrito, CarritoItem
from Menu.models import Producto
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
def mostrar_carrito(request):
    carrito = Carrito.objects.get_or_create(usuario=request.user)[0]
    items_carrito = carrito.carritoitem_set.all()
    
    for item in items_carrito:
        item.subtotal = item.producto.precio * item.cantidad

    def get(self, request, producto_id):
        producto = Producto.objects.get(pk=producto_id)
        carrito, created = Carrito.objects.get_or_create(usuario=request.user, producto=producto)
        carrito.cantidad += 1
        carrito.save()

    total = sum(item.subtotal for item in items_carrito)


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