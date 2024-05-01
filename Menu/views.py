from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Producto, CategoriaMenu
from .forms import ProductoForm, Adicional, AdicionalForm
from django.shortcuts import get_object_or_404

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

    
    def post(self, request, *args, **kwargs):
            form = self.get_form()
            if form.is_valid():
                producto = form.save()  # Save the product first

                
                nombres = request.POST.getlist('nombre_adicional')  
                precios = request.POST.getlist('precio_adicional')  

                for nombre, precio in zip(nombres, precios):
                    adicional = Adicional(nombre=nombre, precio_extra=precio)
                    adicional.save()  # Save the additional object first
                    producto.adicionales.add(adicional.id)

                return redirect('Menu')  # Redirect after successful save
            else:
                # Handle form errors
                return render(request, self.template_name, {'form': form})

    
    def form_valid(self, form):
        
        messages.success(self.request, 'El platillo se ha creado exitosamente.')

        return super().form_valid(form)
    
class ProductoEditarView( LoginRequiredMixin, UpdateView):
    model = Producto
    template_name = 'editar_producto.html'
    context_object_name = 'Producto'
    form_class = ProductoForm
    success_url = reverse_lazy('Menu')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            producto = self.get_object()
            current_adicionales = producto.adicionales.all()

            # Get the selected adicionales from the form
            selected_adicionales = set(request.POST.getlist('adicionales'))

            # Add any new adicionales to the product
            for adicional_id in selected_adicionales:
                adicional = Adicional.objects.get(pk=adicional_id)
                if adicional not in current_adicionales:
                    producto.adicionales.add(adicional)

            # Create any new adicionales that were not selected
            for nombre, precio in zip(request.POST.getlist('nombre_adicional'), request.POST.getlist('precio_adicional')):
                adicional = Adicional(nombre=nombre, precio_extra=precio)
                adicional.save()
                producto.adicionales.add(adicional)

            # Remove any adicionales that are no longer selected
            for adicional in current_adicionales:
                if adicional.id not in selected_adicionales:
                    producto.adicionales.remove(adicional)

            return redirect('Menu')
            
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


class AdicionalListView(ListView):
    model = Adicional
    template_name = 'listar_adicionales.html'
    context_object_name = 'adicionales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datatables_view_name'] = 'adicionales_datatable'
        return context

class AdicionalEliminarView(LoginRequiredMixin, DeleteView):
    model = Adicional
    template_name = 'eliminar_adicional.html'
    success_url = reverse_lazy('listar_adicionales')

    

class AdicionalCrearView(LoginRequiredMixin, CreateView):
    model = Adicional
    template_name = 'crear_adicional.html'
    form_class = AdicionalForm
    success_url = reverse_lazy('listar_adicionales')

   

class AdicionalEditarView(LoginRequiredMixin, UpdateView):
    model = Adicional
    template_name = 'editar_adicional.html'
    form_class = AdicionalForm
    success_url = reverse_lazy('listar_adicionales')

