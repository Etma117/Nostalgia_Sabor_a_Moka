from django.urls import path
from . import views
from .views import HomeDomicilio, HomeView, Carrito_mesa, MostrarCarrito, Carrito_domicilio, EliminarProductoDelCarrito, AgregarCantidadProducto, LimpiarCarritoMesa, PagarCarritoPorMesa, AgregarAlCarritoMesa, SeleccionarMesa

urlpatterns = [
    path('', HomeView.as_view(), name= 'Comanda'),
    path('comanda/<int:categoria_id>/', HomeView.as_view(), name='comanda_por_categoria'),

    path('buscar_productos/', views.buscar_productos, name='buscar_productos'),

    path('comanda_domicilio/', HomeDomicilio.as_view() , name='HomeDomicilio'),

    path('ver_comanda/', MostrarCarrito.as_view(), name='VerComanda'),
    path('eliminar_producto/<int:carrito_item_id>/', EliminarProductoDelCarrito.as_view(), name='eliminar_producto_carrito'),

    path('carrito_por_mesa/<int:mesa_id>', Carrito_mesa.as_view(), name='carrito_por_mesa'),
    path('limpiar-carrito/<int:mesa_id>/', LimpiarCarritoMesa.as_view(), name='limpiar_carrito_por_mesa'),


    path('carrito_pedido_domicilio/', Carrito_domicilio.as_view(), name='carrito_pedido_domicilio'),
    path('agregar_cantidad_producto/<int:carrito_item_id>/', AgregarCantidadProducto.as_view(), name='agregar_cantidad_producto'),

    path('pagar-carrito/<int:mesa_id>/', PagarCarritoPorMesa.as_view(), name='pagar_carrito_por_mesa'),

    path('agregar_por_mesa/', AgregarAlCarritoMesa , name='agregar_por_mesa'),
    path('seleccionar_mesa/', SeleccionarMesa , name='seleccionar_mesa'),

]
