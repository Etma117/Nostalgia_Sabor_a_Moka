from django.urls import path
from . import views
from .views import Productos, mostrar_carrito, añadir_producto_al_carrito, eliminar_producto_del_carrito

urlpatterns = [
    path('', views.home, name= 'Comanda'),
    path('domicilio/', views.domicilio, name='Domicilio'),
    path('salon/', views.salon, name='Salon'),
    path('Productos/', Productos.as_view() , name='Productos'),
    path('carrito/', mostrar_carrito, name='mostrar_carrito'),
    path('añadir_producto/', añadir_producto_al_carrito, name='añadir_producto_al_carrito'),
    path('eliminar_producto/<int:carrito_item_id>/', eliminar_producto_del_carrito, name='eliminar_producto_del_carrito'),
]
