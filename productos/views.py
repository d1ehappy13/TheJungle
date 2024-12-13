from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Producto
from .forms import VentaForm, DetalleVentaForm
from .models import Venta, DetalleVenta, Producto
from django.forms import formset_factory
from django.db.models import Sum, F
from django.utils import timezone




def home(request):
    return render(request, 'productos/home.html')


class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'

class ProductoCreateView(CreateView):
    model = Producto
    template_name = 'productos/producto_form.html'
    fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria']
    success_url = reverse_lazy('producto_list')

class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'productos/producto_form.html'
    fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria']
    success_url = reverse_lazy('producto_list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')

def crear_venta(request):
    DetalleFormSet = formset_factory(DetalleVentaForm, extra=1)
    productos = Producto.objects.all()

    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        formset = DetalleFormSet(request.POST)
        if venta_form.is_valid() and formset.is_valid():
            venta = venta_form.save()
            for detalle_form in formset:
                if detalle_form.cleaned_data:
                    detalle = detalle_form.save(commit=False)
                    detalle.venta = venta
                    detalle.precio_unitario = detalle.producto.precio
                    detalle.save()
            return redirect('venta_list')
    else:
        venta_form = VentaForm()
        formset = DetalleFormSet()

    return render(request, 'productos/venta_form.html', {
        'venta_form': venta_form,
        'formset': formset,
        'productos': productos
    })


def lista_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'productos/venta_list.html', {'ventas': ventas})

def comparar_ventas_mensuales(request):
    hoy = timezone.now()
    hace_12_meses = hoy.replace(year=hoy.year - 1)
    ventas_list = Venta.objects.filter(fecha__gte=hace_12_meses)

    datos_por_mes = {}
    for v in ventas_list:
        mes = v.fecha.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        datos_por_mes.setdefault(mes, 0)
        datos_por_mes[mes] += v.total

    ventas_por_mes_list = sorted(
        [{'mes': k, 'total_mes': v} for k, v in datos_por_mes.items()],
        key=lambda x: x['mes']
    )

    return render(request, 'productos/comparar_ventas.html', {
        'ventas_por_mes': ventas_por_mes_list
    })