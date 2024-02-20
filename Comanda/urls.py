from django.urls import path
from . import views
from .views import AgregarAlCarritoView, VerCarritoView

urlpatterns = [
    path('', views.home, name= 'Comanda'),
    path('domicilio/', views.domicilio, name='Domicilio'),
    path('salon/', views.salon, name='Salon'),
    path('agregar-al-carrito/<int:producto_id>/', AgregarAlCarritoView.as_view(), name='agregar_al_carrito'),
    path('ver-carrito/', VerCarritoView.as_view(), name='carrito'),
]
