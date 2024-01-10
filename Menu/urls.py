from django.contrib import admin
from django.urls import path
from .views import MenuListar, ProductoCrearView, ProductoEditarView, ProductoEliminarView, ProductoDetalle

urlpatterns = [
    path('',MenuListar.as_view() , name= 'Menu'),
    path('crearproducto/',ProductoCrearView.as_view(), name='CrearProducto'),    
    path('editarproducto/<int:pk>/',ProductoEditarView.as_view(), name='EditarProducto'),
    path('eliminarproducto/<int:pk>/',ProductoEliminarView.as_view(), name='EliminarProducto'),    
    path('producto_detalles/<int:pk>/',ProductoDetalle.as_view(), name='DetalleProducto'),

]
