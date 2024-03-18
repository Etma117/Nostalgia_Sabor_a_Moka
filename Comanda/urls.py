from django.urls import path
from . import views
from .views import HomeDomicilio, HomeView, Carrito_mesa, MostrarCarrito, Carrito_Domicilio, EliminarProductoDelCarrito, AgregarCantidadProducto, LimpiarCarritoMesa, PagarCarritoPorMesa, AgregarAlCarritoMesa, SeleccionarMesa, FormularioDomicilio, AgregarAlCarritoDomicilio

urlpatterns = [
    path('', HomeView.as_view(), name= 'Comanda'),    
    path('comanda_domicilio/', HomeDomicilio.as_view() , name='HomeDomicilio'),
    path('buscar_productos/', views.BuscarProductos, name='buscar_productos'),


    path('ver_comanda/', MostrarCarrito.as_view(), name='VerComanda'),
    path('eliminar_producto/<int:carrito_item_id>/', EliminarProductoDelCarrito.as_view(), name='eliminar_producto_carrito'),

    path('carrito_por_mesa/<int:mesa_id>', Carrito_mesa.as_view(), name='carrito_por_mesa'),
    path('limpiar-carrito/<int:mesa_id>/', LimpiarCarritoMesa.as_view(), name='limpiar_carrito_por_mesa'),


   
    path('agregar_cantidad_producto/<int:carrito_item_id>/', AgregarCantidadProducto.as_view(), name='agregar_cantidad_producto'),

    path('pagar-carrito/<int:mesa_id>/', PagarCarritoPorMesa.as_view(), name='pagar_carrito_por_mesa'),



    path('agregar_por_mesa/', AgregarAlCarritoMesa, name='agregar_por_mesa'),
    path('seleccionar_mesa/', SeleccionarMesa , name='seleccionar_mesa'),

    path('carrito_por_domicilio/<int:pedidodomicilio_id>', Carrito_Domicilio.as_view(), name='carrito_por_domicilio'),
    path('agregar_por_domicilio/', AgregarAlCarritoDomicilio, name='agregar_por_domicilio'),
    path('datos_domicilio/', FormularioDomicilio, name='datos_domicilio'),
    
    path('pagar-carrito-domicilio/<int:domicilio_id>/', views.PagarCarritoPorDomicilio.as_view(), name='pagar_carrito_domicilio'),    
    path('limpiar-carrito-domicilio/<int:pedidodomicilio_id>/', views.LimpiarCarritoDomicilio.as_view(), name='limpiar_carrito_domicilio'),

]
