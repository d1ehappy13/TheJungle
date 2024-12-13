"""
URL configuration for TheJungle project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from productos.views import (home, ProductoListView, ProductoCreateView,
                             ProductoUpdateView, ProductoDeleteView,
                             crear_venta, lista_ventas, comparar_ventas_mensuales)  # Asegúrate de importar aquí

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('productos/', ProductoListView.as_view(), name='producto_list'),
    path('productos/crear/', ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/editar/', ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/eliminar/', ProductoDeleteView.as_view(), name='producto_delete'),

    path('ventas/', lista_ventas, name='venta_list'),
    path('ventas/crear/', crear_venta, name='crear_venta'),

    # Aquí la ruta a la vista comparar_ventas_mensuales
    path('ventas/comparar/', comparar_ventas_mensuales, name='comparar_ventas_mensuales'),
]
