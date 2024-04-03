from django.contrib import admin
from django.urls import path
from .views import MenuListar, ProductoCrearView, ProductoEditarView, ProductoEliminarView, ProductoDetalle
from .views import AdicionalCrearView, AdicionalEditarView, AdicionalEliminarView, AdicionalListView

urlpatterns = [
    path('',MenuListar.as_view() , name= 'Menu'),
    path('menu/<int:categoria_id>/', MenuListar.as_view(), name='menu_por_categoria'),
    
    path('crearproducto/',ProductoCrearView.as_view(), name='CrearProducto'),    
    path('editarproducto/<int:pk>/',ProductoEditarView.as_view(), name='EditarProducto'),
    path('eliminarproducto/<int:pk>/',ProductoEliminarView.as_view(), name='EliminarProducto'),    
    path('producto_detalles/<int:pk>/',ProductoDetalle.as_view(), name='DetalleProducto'),

   
    path('crear_adicional/', AdicionalCrearView.as_view(), name='crear_adicional'),
    path('editar_adicional/<int:pk>/', AdicionalEditarView.as_view(), name='editar_adicional'),
    path('eliminar_adicional/<int:pk>/', AdicionalEliminarView.as_view(), name='eliminar_adicional'),
    path('listar_adicionales/', AdicionalListView.as_view(), name='listar_adicionales'),



]
