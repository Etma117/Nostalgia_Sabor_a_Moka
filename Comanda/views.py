<<<<<<< HEAD
from django.shortcuts import render, redirect
=======
from django.shortcuts import render
>>>>>>> 8cfbabb16bc1dc01662fb6a3e2298a4aec853728
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Carrito
from Menu.models import Producto

# Create your views here.
def home(request):
    return render(request, 'comanda.html')

def domicilio(request):
    return render(request, 'domicilio.html')

<<<<<<< HEAD
=======
def salon(request):
    return render(request, 'salon.html')

>>>>>>> 8cfbabb16bc1dc01662fb6a3e2298a4aec853728
class AgregarAlCarritoView(LoginRequiredMixin, View):
    login_url = 'login'  
    redirect_field_name = 'next' 

    def get(self, request, producto_id):
        producto = Producto.objects.get(pk=producto_id)
        carrito, created = Carrito.objects.get_or_create(usuario=request.user, producto=producto)
        carrito.cantidad += 1
        carrito.save()
<<<<<<< HEAD
        return redirect('carrito')
=======
        return redirect('carrito')

class VerCarritoView(LoginRequiredMixin, View):
    login_url = 'login'  
    redirect_field_name = 'next' 

    def get(self, request):
        carrito_items = Carrito.objects.filter(usuario=request.user)
        return render(request, 'carrito.html', {'carrito_items': carrito_items})
>>>>>>> 8cfbabb16bc1dc01662fb6a3e2298a4aec853728
