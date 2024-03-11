from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, View
from Comanda.models import Carrito, CarritoItem, Mesa, PedidoDomicilio
from Menu.models import Producto, CategoriaMenu
from Venta.models import Venta, VentaItem
from django.db.models import Q


from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.http import JsonResponse

def buscar_productos(request):
    query = request.GET.get('q', '')

    resultados = Producto.objects.filter(
        Q(nombre__icontains=query) |
        Q(descripcion__icontains=query) |
        Q(sabores_raw__icontains=query) 
    )

    data = [
        {
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'sabores': producto.obtener_sabores(),
            'precio': float(producto.precio),
            'categoria': producto.categoria.nombreCate if producto.categoria else None,
            'imagen': str(producto.imagen.url) if producto.imagen else None,
            'id': producto.id
            
        } for producto in resultados
        
    ]
    print('Categorias', [item['categoria'] for item in data])
    

    return JsonResponse(data, safe=False)




class BuscadorYCategoriasMixin(View):
    def get_queryset(self):
        categoria_id = self.kwargs.get('categoria_id')
        productos = Producto.objects.all()

        if categoria_id:
            productos = productos.filter(categoria=categoria_id)

        busqueda = self.request.GET.get("Buscar")
        if busqueda:
            atributos_a_buscar = ['nombre', 'descripcion', 'precio', 'categoria__nombreCate']
            query = Q()

            for atributo in atributos_a_buscar:
                query |= Q(**{f'{atributo}__icontains': busqueda})

            productos = productos.filter(query)

        return productos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = CategoriaMenu.objects.all()
        return context


class HomeView(BuscadorYCategoriasMixin, ListView):
    model = Producto
    template_name = 'comanda.html'
    context_object_name = 'productos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mesas'] = Mesa.objects.all()
        return context

class Productos(LoginRequiredMixin, ListView):
    login_url = 'login'  
    redirect_field_name = 'next'
    model = Producto
    template_name = 'Productos.html'
    context_object_name = 'Producto'

class MostrarCarrito(LoginRequiredMixin, View):
    login_url = 'login'  
    redirect_field_name = 'next'
    template_name = 'carrito.html'

    def get(self, request):
        mesas = Mesa.objects.all()
        return render(request, self.template_name, {'mesas': mesas})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class Carrito_mesa(LoginRequiredMixin, View):
    login_url = 'login'  
    redirect_field_name = 'next'
    template_name = 'carrito_mesa.html'

    def get(self, request, mesa_id):
        mesa = get_object_or_404(Mesa, id=mesa_id)
        carrito, created = Carrito.objects.get_or_create(mesa=mesa)
        items_carrito = carrito.carritoitem_set.all()

        for item in items_carrito:
            item.subtotal = item.producto.precio * item.cantidad

        total = sum(item.subtotal for item in items_carrito)

        return render(request, self.template_name, {'items_carrito': items_carrito, 'total': total, 'mesa': mesa, 'carrito': carrito})

    def post(self, request, mesa_id):
        mesa_id = request.POST.get ('mesa_id')
        cantidad = int(request.POST.get('cantidad', 1))

        mesa = get_object_or_404(Mesa, id=mesa_id)
        sabores_seleccionados = request.POST.getlist('sabores')
        producto_ids = request.POST.getlist ('id_producto')

        carrito, created = Carrito.objects.get_or_create(mesa=mesa)
        for producto_id in producto_ids:
            producto = get_object_or_404(Producto, id=producto_id)
            sabores_disponibles = producto.obtener_sabores()

            for sabor in sabores_seleccionados:
                if sabor in sabores_disponibles:
                    carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto, sabor=sabor)

                    if carrito_item:
                        carrito_item.cantidad += cantidad
                        carrito_item.save()
                    else:
                        CarritoItem.objects.create(carrito=carrito, producto=producto, cantidad=cantidad)

        return redirect('Comanda')
    

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
        
        # Ejemplo: Redirigir al carrito de domicilio
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