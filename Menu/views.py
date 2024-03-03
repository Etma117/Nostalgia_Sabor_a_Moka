from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Producto, CategoriaMenu
from .forms import ProductoForm

class BuscadorProductosMixin:
    def buscar(self):
        busqueda = self.request.GET.get("Buscar")
        self.productos = Producto.objects.all()

        if busqueda:
            atributos_a_buscar = ['nombre','descripcion', 'precio', 'categoria__nombreCate']
            query = Q()

            for atributo in atributos_a_buscar:
                query |= Q(**{f'{atributo}__icontains': busqueda})

            self.productos = self.productos.filter(query)

    def get_context_data(self, **kwargs):
        self.buscar()
        context = super().get_context_data(**kwargs)
        context['Productos'] = self.productos
        return context


class MenuListar( BuscadorProductosMixin, ListView, LoginRequiredMixin ):
    login_url = 'login'  
    redirect_field_name = 'next' 

    model = Producto
    template_name = 'Menu.html'
    context_object_name = 'Productos'       
    
    def get_queryset(self):
        categoria_id = self.kwargs.get('categoria_id')
        if categoria_id:
            return Producto.objects.filter(categoria=categoria_id)
        else:
            return Producto.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = CategoriaMenu.objects.all()
        return context

    

class ProductoCrearView(CreateView, LoginRequiredMixin):
    model = Producto
    template_name = 'crear_producto.html'
    context_object_name = 'Producto'
    form_class = ProductoForm
    success_url = reverse_lazy('Menu')
    
    def form_valid(self, form):
        messages.success(self.request, 'El platillo se ha creado exitosamente.')
        return super().form_valid(form)
    
class ProductoEditarView(UpdateView, LoginRequiredMixin):
    model = Producto
    template_name = 'editar_producto.html'
    context_object_name = 'Producto'
    form_class = ProductoForm
    success_url = reverse_lazy('Menu')
    
    def form_valid(self, form):
        messages.success(self.request, 'El platillo se ha editado exitosamente.')
        return super().form_valid(form)
    

class ProductoEliminarView(DeleteView, LoginRequiredMixin):
    model = Producto
    template_name = 'eliminar_producto.html'
    context_object_name = 'Producto'
    success_url = reverse_lazy('Menu')

    def form_valid(self, form):
        messages.error(self.request, 'El platillo se ha dado de baja del menú.')
        return super().form_valid(form)


class ProductoDetalle(DetailView, LoginRequiredMixin):
    model = Producto
    template_name = 'producto_detalle.html'
    context_object_name = 'Producto'  # Nombre de la variable en la plantilla
    pk_url_kwarg = 'producto_id'  # Nombre del parámetro en la URL