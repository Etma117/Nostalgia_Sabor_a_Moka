from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Carrito, CarritoItem, Mesa, PedidoDomicilio
from Menu.models import Producto
from django.contrib.auth.models import User
from django.views import View

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


# class MostrarCarrito(View):
#     template_name = 'carrito.html'

#     def get(self, request):
#         carrito = Carrito.objects.get_or_create(usuario=request.user)[0]
#         items_carrito = carrito.carritoitem_set.all()

#         for item in items_carrito:
#             item.subtotal = item.producto.precio * item.cantidad

#         total = sum(item.subtotal for item in items_carrito)

#         return render(request, self.template_name, {'items_carrito': items_carrito, 'total': total})
    

class MostrarCarrito(View):
    template_name = 'carrito.html'

    def get(self, request):
        mesas = Mesa.objects.all()
        pedidos_domicilio = PedidoDomicilio.objects.all()

        return render(request, self.template_name, {'mesas': mesas, 'pedidos_domicilio': pedidos_domicilio})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MostrarCarritoPorMesaView(View):
    template_name = 'carrito.html'

    def get(self, request, mesa_id):
        mesa = get_object_or_404(Mesa, id=mesa_id)
        carrito = Carrito.objects.get_or_create(mesa=mesa)[0]
        items_carrito = carrito.carritoitem_set.all()

        for item in items_carrito:
            item.subtotal = item.producto.precio * item.cantidad

        total = sum(item.subtotal for item in items_carrito)

        return render(request, self.template_name, {'items_carrito': items_carrito, 'total': total})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MostrarCarritoPedidoDomicilioView(View):
    template_name = 'carrito.html'

    def get(self, request):
        pedido_domicilio = PedidoDomicilio.objects.first()  # Puedes ajustar esta lógica según tus necesidades
        carrito = Carrito.objects.get_or_create(pedido_domicilio=pedido_domicilio)[0]
        items_carrito = carrito.carritoitem_set.all()

        for item in items_carrito:
            item.subtotal = item.producto.precio * item.cantidad

        total = sum(item.subtotal for item in items_carrito)

        return render(request, self.template_name, {'items_carrito': items_carrito, 'total': total})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AñadirProductoAlCarrito(View):
    def post(self, request):
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

class EliminarProductoDelCarrito(View):
    def post(self, request, carrito_item_id):
        carrito_item = get_object_or_404(CarritoItem, id=carrito_item_id)

        if carrito_item.carrito.usuario == request.user:
            carrito_item.delete()

        return redirect('mostrar_carrito') 