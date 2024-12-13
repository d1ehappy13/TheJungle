from django.db import models
from django.utils import timezone

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    numero_boleta = models.CharField(max_length=50, unique=True)  # número único de boleta
    fecha = models.DateTimeField(default=timezone.now)
    # Podríamos agregar campos como cliente, vendedor, etc. según sea necesario

    @property
    def total(self):
        # Calcula el total sumando los subtotales de cada detalle
        return sum(detalle.subtotal for detalle in self.detalles.all())

    def __str__(self):
        return f"Venta {self.numero_boleta} - {self.fecha.strftime('%d/%m/%Y')}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
