from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Producto, CategoriaMenu
from .forms import ProductoForm

class BuscadorYCategoriasMixin():
     

    def get_queryset(self):
        categoria_id = self.kwargs.get('categoria_id')
        productos = Producto.objects.all()

        if categoria_id:
            productos = productos.filter(categoria=categoria_id)

        busqueda = self.request.GET.get("Buscar")
        if busqueda:
            atributos_a_buscar = ['nombre', 'descripcion', 'precio', 'categoria__nombreCate']
            query = Q()

            for atributo in atributos_a_buscar:
                query |= Q(**{f'{atributo}__icontains': busqueda})

            productos = productos.filter(query)

        return productos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = CategoriaMenu.objects.all()
        return context

class MenuListar(LoginRequiredMixin, BuscadorYCategoriasMixin, ListView):
    login_url = 'login'  
    redirect_field_name = 'next'

    model = Producto
    template_name = 'Menu.html'
    context_object_name = 'Productos'
    

class ProductoCrearView(LoginRequiredMixin, CreateView ):
    model = Producto
    template_name = 'crear_producto.html'
    context_object_name = 'Producto'
    form_class = ProductoForm
    success_url = reverse_lazy('Menu')
    
    def form_valid(self, form):
        messages.success(self.request, 'El platillo se ha creado exitosamente.')
        return super().form_valid(form)
    
class ProductoEditarView( LoginRequiredMixin, UpdateView):
    model = Producto
    template_name = 'editar_producto.html'
    context_object_name = 'Producto'
    form_class = ProductoForm
    success_url = reverse_lazy('Menu')
    
    def form_valid(self, form):
        messages.success(self.request, 'El platillo se ha editado exitosamente.')
        return super().form_valid(form)
    

class ProductoEliminarView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'eliminar_producto.html'
    context_object_name = 'Producto'
    success_url = reverse_lazy('Menu')

    def form_valid(self, form):
        messages.error(self.request, 'El platillo se ha dado de baja del menú.')
        return super().form_valid(form)


class ProductoDetalle(LoginRequiredMixin, DetailView ):
    model = Producto
    template_name = 'producto_detalle.html'
    context_object_name = 'Producto'  # Nombre de la variable en la plantilla
    pk_url_kwarg = 'producto_id'  # Nombre del parámetro en la URL