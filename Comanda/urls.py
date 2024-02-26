from django.urls import path
from . import views
from .views import Productos, MostrarCarrito, AñadirProductoAlCarrito, EliminarProductoDelCarrito

urlpatterns = [
    path('', views.home, name= 'Comanda'),
    path('domicilio/', views.domicilio, name='Domicilio'),
    path('salon/', views.salon, name='Salon'),
    path('Productos/', Productos.as_view() , name='Productos'),
    path('carrito/', MostrarCarrito.as_view(), name='mostrar_carrito'),
    path('añadir_producto/', AñadirProductoAlCarrito.as_view(), name='añadir_producto_al_carrito'),
    path('eliminar_producto_del_carrito/<int:carrito_item_id>/', EliminarProductoDelCarrito.as_view(), name='eliminar_producto_del_carrito'),
]
