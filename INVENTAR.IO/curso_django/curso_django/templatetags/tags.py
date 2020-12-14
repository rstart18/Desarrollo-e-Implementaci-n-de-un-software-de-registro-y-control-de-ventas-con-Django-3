from django import template
from Almacen.models import Productos

register = template.Library()

@register.simple_tag()
def multiply(a,b):
       return a * b

@register.simple_tag()
def product_img(id):
       imagen = Productos.objects.get(id=id).imagen
       return imagen

@register.simple_tag()
def turned(n):
       return n