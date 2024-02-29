from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, View
from Comanda.models import Carrito, CarritoItem, Mesa, PedidoDomicilio
from Menu.models import Producto

# Create your views here.
def home(request):
    mesas = Mesa.objects.all()
    productos = Producto.objects.all()
    return render(request, 'comanda.html', {'mesas': mesas, 'productos':productos})

def domicilio(request):
    return render(request, 'domicilio.html')

def salon(request):
    return render(request, 'salon.html')

class Productos(ListView):
    model = Producto
    template_name = 'Productos.html'
    context_object_name = 'Producto'

class MostrarCarrito(View):
    template_name = 'carrito.html'

    def get(self, request):
        mesas = Mesa.objects.all()
        return render(request, self.template_name, {'mesas': mesas})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class Carrito_mesa(View):
    template_name = 'carrito.html'

    def get(self, request, mesa_id):
        mesa = get_object_or_404(Mesa, id=mesa_id)
        carrito, created = Carrito.objects.get_or_create(mesa=mesa)
        items_carrito = carrito.carritoitem_set.all()

        for item in items_carrito:
            item.subtotal = item.producto.precio * item.cantidad

        total = sum(item.subtotal for item in items_carrito)

        return render(request, self.template_name, {'items_carrito': items_carrito, 'total': total, 'mesa': mesa, 'carrito': carrito})

    def post(self, request, mesa_id):
        producto_id = request.POST.get ('id_producto')
        mesa_id = request.POST.get ('mesa_id')
        cantidad = int(request.POST.get('cantidad', 1))

        producto = get_object_or_404(Producto, id=producto_id)
        mesa = get_object_or_404(Mesa, id=mesa_id)
        sabores_seleccionados = request.POST.getlist('sabores')

        carrito, created = Carrito.objects.get_or_create(mesa=mesa)
        for sabor in sabores_seleccionados:
            carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto, sabor=sabor)

            if carrito_item:
                carrito_item.cantidad += cantidad
                carrito_item.save()
            else:
                CarritoItem.objects.create(carrito=carrito, producto=producto, cantidad=cantidad)

        return redirect('Comanda')

class Carrito_domicilio (View):
    template_name = 'carrito.html'

    def get(self, request):
        pedido_domicilio = PedidoDomicilio.objects.first()
        carrito, created = Carrito.objects.get_or_create(pedido_domicilio=pedido_domicilio)
        items_carrito = carrito.carritoitem_set.all()

        for item in items_carrito:
            item.subtotal = item.producto.precio * item.cantidad

        total = sum(item.subtotal for item in items_carrito)

        return render(request, self.template_name, {'items_carrito': items_carrito, 'total': total, 'pedido_domicilio': pedido_domicilio, 'carrito':carrito})

    def post(self, request):
        producto_id = request.POST.get ('id_producto')
        cantidad = int(request.POST.get('cantidad', 1))

        producto = get_object_or_404(Producto, id=producto_id)
        pedido_domicilio = PedidoDomicilio.objects.first()
        sabores_seleccionados = request.POST.getlist('sabores')

        carrito, created = Carrito.objects.get_or_create(pedido_domicilio=pedido_domicilio)
        for sabor in sabores_seleccionados:
            carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto, sabor=sabor)

            if carrito_item:
                carrito_item.cantidad += cantidad
                carrito_item.save()
            else:
                CarritoItem.objects.create(carrito=carrito, producto=producto, cantidad=cantidad)

        return redirect('Comanda')

class EliminarProductoDelCarrito(View):
    def post(self, request, carrito_item_id):
        carrito_item = get_object_or_404(CarritoItem, id=carrito_item_id)
        carrito_item.delete()

        if hasattr(carrito_item, 'carrito') and carrito_item.carrito:
            return redirect('carrito_por_mesa', mesa_id=carrito_item.carrito.mesa.id)
        
        # Ejemplo: Redirigir al carrito de domicilio
        if hasattr(carrito_item, 'pedido_domicilio') and carrito_item.pedido_domicilio:
            return redirect('carrito_pedido_domicilio')
        
        return redirect('MostrarCarrito')

class AgregarCantidadProducto(View):
    def post(self, request, carrito_item_id):
        carrito_item = get_object_or_404(CarritoItem, id=carrito_item_id)
        nueva_cantidad = int(request.POST.get('nueva_cantidad', 1))
        carrito_item.cantidad += nueva_cantidad
        carrito_item.save()

        if hasattr(carrito_item, 'carrito') and carrito_item.carrito:
            return redirect('carrito_por_mesa', mesa_id=carrito_item.carrito.mesa.id)
            
        # Ejemplo: Redirigir al carrito de domicilio
        if hasattr(carrito_item, 'pedido_domicilio') and carrito_item.pedido_domicilio:
            return redirect('carrito_pedido_domicilio')

        return redirect('MostrarCarrito') 