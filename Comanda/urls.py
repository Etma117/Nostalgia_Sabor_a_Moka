from django.urls import path
from . import views
from .views import Productos

urlpatterns = [
    path('', views.home, name= 'Comanda'),
    path('domicilio/', views.domicilio, name='Domicilio'),
    path('salon/', views.salon, name='Salon'),
    path('Productos/', Productos.as_view() , name='Productos'),
    path('ver-carrito/', views.Carrito, name='ver_carrito'),
    path('agregar-producto/', views.AgregarAlCarrito, name='agregar_producto_al_carrito'),
]
