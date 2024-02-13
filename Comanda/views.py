from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'comanda.html')

def domicilio(request):
    return render(request, 'domicilio.html')