import json
from django.contrib import admin
from django import forms
from django.forms import CharField
from .models import Producto

class ProductoForm(forms.ModelForm):
    sabores = CharField()

    class Meta:
        model = Producto
        fields = '__all__'

    def clean_sabores(self):
        sabores_input = self.cleaned_data.get('sabores')
        try:
            # Intenta convertir la entrada a una lista y luego a JSON
            return json.dumps([sabor.strip() for sabor in sabores_input.split(',')])
        except json.JSONDecodeError:
            raise forms.ValidationError("Formato de sabores no válido. Ingrese una lista separada por comas.")

class ProductoAdmin(admin.ModelAdmin):
    form = ProductoForm
