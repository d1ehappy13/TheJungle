from django import forms
from .models import Venta, DetalleVenta, Producto
from django.forms import formset_factory


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['numero_boleta', 'fecha']

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }