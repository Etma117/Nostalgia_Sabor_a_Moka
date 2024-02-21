from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Carrito
from Menu.models import Producto

# Create your views here.
def home(request):
    return render(request, 'comanda.html')

def domicilio(request):
    return render(request, 'domicilio.html')

class AgregarAlCarritoView(LoginRequiredMixin, View):
    login_url = 'login'  
    redirect_field_name = 'next' 

    def get(self, request, producto_id):
        producto = Producto.objects.get(pk=producto_id)
        carrito, created = Carrito.objects.get_or_create(usuario=request.user, producto=producto)
        carrito.cantidad += 1
        carrito.save()
        return redirect('carrito')