from django.urls import path
from . import views
<<<<<<< HEAD
from .views import AgregarAlCarritoView
urlpatterns = [
    path('', views.home, name= 'Comanda'),
    path('domicilio/', views.domicilio, name='Domicilio'),
    path('agregar-al-carrito/<int:producto_id>/', AgregarAlCarritoView.as_view(), name='agregar_al_carrito'),
=======
from .views import AgregarAlCarritoView, VerCarritoView

urlpatterns = [
    path('', views.home, name= 'Comanda'),
    path('domicilio/', views.domicilio, name='Domicilio'),
    path('salon/', views.salon, name='Salon'),
    path('agregar-al-carrito/<int:producto_id>/', AgregarAlCarritoView.as_view(), name='agregar_al_carrito'),
    path('ver-carrito/', VerCarritoView.as_view(), name='carrito'),
>>>>>>> 8cfbabb16bc1dc01662fb6a3e2298a4aec853728
]
