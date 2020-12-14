from django.contrib import admin

from gestionVenta.models import Ventas,Facturas,Envios
from Almacen.models import Proveedores,Categorias,Productos

# Register your models here.

admin.site.register(Proveedores)
admin.site.register(Categorias)
admin.site.register(Productos)

admin.site.register(Ventas)
admin.site.register(Facturas)
admin.site.register(Envios)