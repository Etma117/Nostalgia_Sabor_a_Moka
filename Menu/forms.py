from django import forms
from django.forms import inlineformset_factory
from .models import Producto, Adicional

class AdicionalForm(forms.ModelForm):
    class Meta:
        model = Adicional
        fields = ['nombre', 'precio_extra']
        labels = {
            'nombre': 'Nombre del Adicional',
            'precio_extra': 'Precio Extra'
        }
        widgets ={
            'nombre': forms.TextInput(attrs={'class':'form-control'}),                   
            'precio' : forms.NumberInput(attrs={'class': 'form-control'}),            
           
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__' #nombre, descripcion, sabores_raw, precio, categoria, imagen 
        labels = {
            'nombre': 'Nombre del Platillo o Bebida',
            'descripcion': 'Descripción Breve',
            'sabores_raw': 'Sabores: inserte los sabores separados por una coma.',
            'precio':'Precio Unitario',
            'categoria':'Categoria',
            'imagen':'Imagen Representativa',
            'adicionales':'Ingredientes Adicionales (Mantenga presionado "Control" o "Comando" en una Mac, para seleccionar o deseleccionar más de uno. O agrege uno abajo)'
        }
        widgets ={
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion' : forms.TextInput(attrs={'class': 'form-control'}),
            'sabores_raw': forms.TextInput(attrs={'class':'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),            
            'precio' : forms.NumberInput(attrs={'class': 'form-control'}),            
            'imagen' : forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg', 
                                                       'id':'formFileLg' }),
            'adicionales':forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
     

    

