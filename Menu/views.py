from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Producto
from .forms import ProductoForm

class MenuListar(ListView):
    model = Producto
    template_name = 'Menu.html'
    context_object_name = 'Producto'
    

class ProductoCrearView(CreateView):
    model = Producto
    template_name = 'crear_producto.html'
    context_object_name = 'Producto'
    form_class = ProductoForm
    
    def form_valid(self, form):
        messages.success(self.request, 'El objeto se ha Creado exitosamente.')
        return super().form_valid(form)