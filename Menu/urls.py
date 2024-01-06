from django.contrib import admin
from django.urls import path
from .views import MenuListar, ProductoCrearView

urlpatterns = [
    path('',MenuListar.as_view() , name= 'Menu'),
    path('crearproducto/',ProductoCrearView.as_view(), name='CrearProducto'),

]
