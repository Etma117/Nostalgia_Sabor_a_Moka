from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Producto, CategoriaMenu
from .forms import ProductoForm


@method_decorator(login_required, name='dispatch')
class MenuListar(ListView):
    model = Producto
    template_name = 'Menu.html'
    context_object_name = 'Producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = CategoriaMenu.objects.all()
        return context

    

class ProductoCrearView(CreateView):
    model = Producto
    template_name = 'crear_producto.html'
    context_object_name = 'Producto'
    form_class = ProductoForm
    success_url = reverse_lazy('Menu')
    
    def form_valid(self, form):
        messages.success(self.request, 'El platillo se ha creado exitosamente.')
        return super().form_valid(form)
    
class ProductoEditarView(UpdateView):
    model = Producto
    template_name = 'editar_producto.html'
    context_object_name = 'Producto'
    form_class = ProductoForm
    success_url = reverse_lazy('Menu')
    
    def form_valid(self, form):
        messages.success(self.request, 'El platillo se ha editado exitosamente.')
        return super().form_valid(form)
    

class ProductoEliminarView(DeleteView):
    model = Producto
    template_name = 'eliminar_producto.html'
    context_object_name = 'Producto'
    success_url = reverse_lazy('Menu')

    def form_valid(self, form):
        messages.error(self.request, 'El platillo se ha dado de baja del menú.')
        return super().form_valid(form)


class ProductoDetalle(DetailView):
    model = Producto
    template_name = 'producto_detalle.html'
    context_object_name = 'Producto'  # Nombre de la variable en la plantilla
    pk_url_kwarg = 'producto_id'  # Nombre del parámetro en la URL