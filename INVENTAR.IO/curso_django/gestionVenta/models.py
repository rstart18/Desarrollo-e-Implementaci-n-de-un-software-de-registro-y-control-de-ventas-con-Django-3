from datetime import datetime
from django.db import models
from Usuarios.models import User


class Facturas(models.Model):
    reference = models.CharField('Referencia',max_length=10,blank=False,null=False,default="",unique=True)
    number = models.IntegerField('Numero de Productos', null=False, blank=False, default=0)
    products = models.CharField('Productos',max_length=250,blank=False,null=False,default="")
    units = models.CharField('Unidades',max_length=250,blank=False,null=False,default="")
    prices = models.CharField('Precios',max_length=250,blank=False,null=False,default="")
    seller = models.CharField('Vendedor',max_length=10,default="")
    discount = models.IntegerField('Descuento',default=0)
    total = models.IntegerField('Total',null=False,blank=False,default=0)
    turned = models.IntegerField('Vueltos',null=False,blank=False,default=0)
    date = models.DateTimeField('Fecha',default=datetime.now())

    def __str__(self):
        return self.reference

class Ventas(models.Model):
    fact = models.ForeignKey(Facturas,on_delete=models.CASCADE, default='', blank=False)
    cliente = models.ForeignKey(User,on_delete=models.CASCADE, default='', blank=False)

    def __str__(self):
        return f"{self.fact} - {self.cliente}"

class Envios(models.Model):
    no_envio = models.CharField('Numero de envio',max_length=10,blank=False,null=False,default=0)
    status = models.CharField('Estado',max_length=20,blank=False,null=False,default='')
    sale = models.ForeignKey(Ventas,on_delete=models.CASCADE, default='', blank=False)