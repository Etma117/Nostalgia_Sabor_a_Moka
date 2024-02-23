from django.urls import path
from . import views
<<<<<<< HEAD
from .views import Productos
=======
from .views import Productos, mostrar_carrito, añadir_producto_al_carrito, eliminar_producto_del_carrito
>>>>>>> e4e796027b5578c93ccdb4fcc368d9ec7b9c18d9

urlpatterns = [
    path('', views.home, name= 'Comanda'),
    path('domicilio/', views.domicilio, name='Domicilio'),
    path('salon/', views.salon, name='Salon'),
    path('Productos/', Productos.as_view() , name='Productos'),
<<<<<<< HEAD
    path('ver-carrito/', views.Carrito, name='ver_carrito'),
    path('agregar-producto/', views.AgregarAlCarrito, name='agregar_producto_al_carrito'),
=======
    path('carrito/', mostrar_carrito, name='mostrar_carrito'),
    path('añadir_producto/', añadir_producto_al_carrito, name='añadir_producto_al_carrito'),
    path('eliminar_producto/<int:carrito_item_id>/', eliminar_producto_del_carrito, name='eliminar_producto_del_carrito'),
>>>>>>> e4e796027b5578c93ccdb4fcc368d9ec7b9c18d9
]
