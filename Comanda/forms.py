from django import forms

class SeleccionSaboresForm(forms.Form):
    sabores = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)