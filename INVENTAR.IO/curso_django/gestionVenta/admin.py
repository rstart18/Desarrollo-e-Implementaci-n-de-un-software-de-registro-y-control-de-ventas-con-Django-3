from django.contrib import admin

from gestionVenta.models import Clientes,Proveedores,Ventas
from Almacen.models import Categorias,Productos

# Register your models here.

admin.site.register(Clientes)
admin.site.register(Proveedores)
admin.site.register(Ventas)

admin.site.register(Categorias)
admin.site.register(Productos)