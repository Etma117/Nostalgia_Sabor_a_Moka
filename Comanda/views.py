from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, View
from Comanda.models import Carrito, CarritoItem, Mesa, PedidoDomicilio
from Menu.models import Producto, CategoriaMenu
from Venta.models import Venta, VentaItem
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin,  ListView):    
    login_url = 'login'  
    redirect_field_name = 'next'
    model = Producto
    template_name = 'comanda.html'
    context_object_name = 'productos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mesas'] = Mesa.objects.all()
        return context

class HomeDomicilio(LoginRequiredMixin, ListView):
    login_url = 'login'  
    redirect_field_name = 'next'
    model = Producto
    template_name = 'domicilio_comanda.html'
    context_object_name = 'Producto'

class MostrarCarrito(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'
    template_name = 'comandas.html'

    def get(self, request):
        mesas = Mesa.objects.all()
        carritos_mesas = []

        for mesa in mesas:
            carrito = Carrito.objects.filter(mesa=mesa).first()
            if carrito:
                productos_carrito = CarritoItem.objects.filter(carrito=carrito)
                carritos_mesas.append({'mesa': mesa, 'productos_carrito': productos_carrito, 'mesa_id': mesa.id})

        # Obtener los carritos de domicilio
        pedidos_domicilio = PedidoDomicilio.objects.all()
        carritos_domicilio = []

        for pedido_domicilio in pedidos_domicilio:
            carrito_domicilio = Carrito.objects.filter(pedido_domicilio=pedido_domicilio).first()
            if carrito_domicilio:
                productos_carrito_domicilio = CarritoItem.objects.filter(carrito=carrito_domicilio)
                carritos_domicilio.append({'pedido_domicilio': pedido_domicilio, 'productos_carrito_domicilio': productos_carrito_domicilio, 'pedido_domicilio_id': pedido_domicilio.id})

        return render(request, self.template_name, {'carritos_mesas': carritos_mesas, 'carritos_domicilio': carritos_domicilio})

class Carrito_mesa(LoginRequiredMixin, View):
    login_url = 'login'  
    redirect_field_name = 'next'
    template_name = 'carrito.html'

    def get(self, request, mesa_id):
        mesa = get_object_or_404(Mesa, id=mesa_id)
        carrito, created = Carrito.objects.get_or_create(mesa=mesa)
        items_carrito = carrito.carritoitem_set.all()

        for item in items_carrito:
            item.subtotal = item.producto.precio * item.cantidad

        total = sum(item.subtotal for item in items_carrito)

        return render(request, self.template_name, {'items_carrito': items_carrito, 'total': total, 'mesa': mesa, 'carrito': carrito})
    

class LimpiarCarritoMesa(View):
    def post(self, request, mesa_id):
        mesa = get_object_or_404(Mesa, id=mesa_id)
        carrito = Carrito.objects.filter(mesa=mesa).first()

        if carrito:
            # Eliminar todos los elementos del carrito
            carrito.carritoitem_set.all().delete()

        return redirect('VerComanda')
    
class PagarCarritoPorMesa(View):
    template_name = 'detalle_venta.html'

    def post(self, request, mesa_id):
        mesa = get_object_or_404(Mesa, id=mesa_id)
        carrito = Carrito.objects.filter(mesa=mesa).first()

        if carrito:
            # Obtener los elementos del carrito antes de limpiarlo
            items_carrito = carrito.carritoitem_set.all()

            # Crear una nueva venta con los datos del carrito
            venta = Venta.objects.create(
                mesa=mesa,
                total=carrito.obtener_total(),
            )

            # Copiar los elementos del carrito a la venta
            for item in items_carrito:
                VentaItem.objects.create(
                    venta=venta,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    subtotal=item.subtotal,
                )

            # Limpiar el carrito
            carrito.carritoitem_set.all().delete()

            # Renderizar una página con el detalle de la venta
            return render(request, self.template_name, {'venta': venta, 'items_carrito': items_carrito})

        return redirect('VerComanda')


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
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        numero = request.POST.get('numero')
        cantidad = int(request.POST.get('cantidad', 1))

        producto_ids = request.POST.getlist('id_producto')
        pedido_domicilio, created_pedido = PedidoDomicilio.objects.get_or_create(nombre=nombre,direccion=direccion,telefono=numero)
        sabores_seleccionados = request.POST.getlist('sabores')

        carrito, created = Carrito.objects.get_or_create(pedido_domicilio=pedido_domicilio)
        for producto_id in producto_ids:
            producto = get_object_or_404(Producto, id=producto_id)
            sabores_disponibles = producto.sabores
            for sabor in sabores_seleccionados:
                if sabor in sabores_disponibles:
                        carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto, sabor=sabor)

                        if carrito_item:
                            carrito_item.cantidad += cantidad
                            carrito_item.save()
                        else:
                            CarritoItem.objects.create(carrito=carrito, producto=producto, cantidad=cantidad)

        return redirect('Comanda')

class EliminarProductoDelCarrito(LoginRequiredMixin, View):
    login_url = 'login'  
    redirect_field_name = 'next'

    def post(self, request, carrito_item_id):
        carrito_item = get_object_or_404(CarritoItem, id=carrito_item_id)
        carrito = carrito_item.carrito
        carrito_item.delete()

        if carrito and carrito.mesa:
            return redirect('carrito_por_mesa', mesa_id=carrito_item.carrito.mesa.id)
        
        if carrito and carrito.pedido_domicilio:
            return redirect('carrito_pedido_domicilio')
        
        return redirect('MostrarCarrito')

class AgregarCantidadProducto(LoginRequiredMixin, View):
    login_url = 'login'  
    redirect_field_name = 'next'

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

        return redirect('VerComanda') 
    
def SeleccionarMesa(request):
    if request.method == 'POST':
        mesa_seleccionada_id = request.POST.get('mesa_seleccionada')
        mesa = get_object_or_404(Mesa, id=mesa_seleccionada_id) 

        productos = obtener_tu_lista_de_productos_actualizada()
        return render(request, 'comanda.html', {'mesas_seleccionadas': mesa, 'productos':productos})
    else:
        mesas = Mesa.objects.all()
        return render(request, 'mesas.html', {'mesas': mesas})

def obtener_tu_lista_de_productos_actualizada():
    return Producto.objects.all()
    

def AgregarAlCarritoMesa(request):
    if request.method == 'POST':
        mesa_id = request.POST.get('mesa_id')
        mesa = get_object_or_404(Mesa, id=mesa_id) 

        for mesa_id in mesa_id:
            producto_id = request.POST.get(f'id_producto_{mesa_id}')
            cantidad = int(request.POST.get(f'cantidad_{mesa_id}', 1))
            sabores_seleccionados = request.POST.getlist(f'sabores_{mesa_id}[]')
            comentario = request.POST.get(f'comentario_{mesa_id}')
            mesa = get_object_or_404(Mesa, id=mesa_id)
            producto = get_object_or_404(Producto, id=producto_id)

            carrito, created = Carrito.objects.get_or_create(mesa=mesa)

            for sabor in sabores_seleccionados:
                carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto, sabor=sabor, comentario=comentario)

                if carrito_item:
                    carrito_item.cantidad += cantidad
                    carrito_item.save()
                else:
                    CarritoItem.objects.create(carrito=carrito, producto=producto, cantidad=cantidad, comentario=comentario)

        productos = obtener_tu_lista_de_productos_actualizada()
        return render(request, 'comanda.html', {'productos': productos, 'mesas_seleccionadas': mesa})
    
    
    # Manejar el caso en que el método de solicitud no sea POST
    return render(request, 'comanda.html')

def BuscarProductos(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        productos = Producto.objects.filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query))
        # Obtener la mesa seleccionada
        mesa_id = request.POST.get('mesa_id')
        mesa = get_object_or_404(Mesa, id=mesa_id) 

        return render(request, 'comanda.html', {'productos': productos, 'mesas_seleccionadas': mesa})

    # Manejar el caso en que el método de solicitud no sea POST
    return render(request, 'comanda.html')






class Carrito_Domicilio(LoginRequiredMixin, View):
    login_url = 'login'  
    redirect_field_name = 'next'
    template_name = 'carrito.html'

    def get(self, request, pedidodomicilio_id):
        domicilio = get_object_or_404(PedidoDomicilio, id=pedidodomicilio_id)
        carrito, created = Carrito.objects.get_or_create(pedido_domicilio=domicilio)
        items_carrito = carrito.carritoitem_set.all()

        for item in items_carrito:
            item.subtotal = item.producto.precio * item.cantidad

        total = sum(item.subtotal for item in items_carrito)

        return render(request, self.template_name, {'items_carrito': items_carrito, 'total': total, 'pedido_domicilio' :domicilio, 'carrito': carrito})
    

def FormularioDomicilio(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        numero_telefono = request.POST.get('numero')
        
        pedido_domicilio = PedidoDomicilio.objects.create(
            nombre=nombre,
            direccion=direccion,
            telefono=numero_telefono
        )

        id_pedido_domicilio = pedido_domicilio.id
        productos = Producto.objects.all()

        return render(request, 'productos_domicilio.html', {'id_pedido_domicilio': id_pedido_domicilio, 'productos': productos})

    return render(request, 'domicilio_comanda.html')
    
def AgregarAlCarritoDomicilio(request):
    if request.method == 'POST':
        pedido_domicilio_id = request.POST.get('id_pedido_domicilio')
        producto_id = request.POST.get('id_producto')
        cantidad = int(request.POST.get('cantidad',1))
        sabores_seleccionados = request.POST.getlist('sabores')
        comentario = request.POST.get('comentario')
        producto = get_object_or_404(Producto, id=producto_id)
        pedido_domicilio = get_object_or_404(PedidoDomicilio, id=pedido_domicilio_id)

        carrito, created = Carrito.objects.get_or_create(pedido_domicilio=pedido_domicilio)

        for sabor in sabores_seleccionados:
            carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto, sabor=sabor, comentario=comentario)

            if carrito_item:
                carrito_item.cantidad += cantidad
                carrito_item.save()
            else:
                CarritoItem.objects.create(carrito=carrito, producto=producto, cantidad=cantidad, comentario=comentario)

        productos = obtener_tu_lista_de_productos_actualizada()
        return render(request, 'productos_domicilio.html', {'productos': productos, 'id_pedido_domicilio': pedido_domicilio_id, 'pedido_domicilio': pedido_domicilio})

    return render(request, 'productos_domicilio.html')

class LimpiarCarritoDomicilio(View):
    def post(self, request, pedidodomicilio_id):
        domicilio = get_object_or_404(PedidoDomicilio, id=pedidodomicilio_id)
        carrito = Carrito.objects.filter(pedido_domicilio=domicilio).first()

        if carrito:
            carrito.carritoitem_set.all().delete()
            carrito.delete()            
            domicilio.delete()

        return redirect('VerComanda')
    
class PagarCarritoPorDomicilio(View):
    template_name = 'detalle_venta_domicilio.html'

    def post(self, request, domicilio_id):
        domicilio = get_object_or_404(PedidoDomicilio, id=domicilio_id)
        
        carrito = Carrito.objects.filter(pedido_domicilio=domicilio).first()

        if carrito:
            # Obtener los elementos del carrito antes de limpiarlo
            items_carrito = carrito.carritoitem_set.all()

            # Crear una nueva venta con los datos del carrito
            venta = Venta.objects.create(
                pedido_domicilio=domicilio,
                total=carrito.obtener_total(),
            )

            # Copiar los elementos del carrito a la venta
            for item in items_carrito:
                VentaItem.objects.create(
                    venta=venta,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    subtotal=item.subtotal,
                )

            # Limpiar el carrito
            carrito.carritoitem_set.all().delete()
            carrito.delete()
            domicilio.delete()


            nombre_domicilio = domicilio.nombre  
            return render(request, self.template_name, {'venta': venta, 'items_carrito': items_carrito, 'nombre_domicilio': nombre_domicilio})

        return redirect('VerComanda')