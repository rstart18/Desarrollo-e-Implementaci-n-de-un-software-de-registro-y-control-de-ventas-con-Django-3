from django.db import models

# Create your models here.

class Categorias(models.Model):
    name = models.CharField('Nombre',max_length=20,unique=True)
    reference = models.CharField('Referencia',max_length=10,blank=False,unique=True,null=True)

    def __str__(self):
        return self.name



class Proveedores(models.Model):
    enterprise_name = models.CharField('Nombre de la empresa',max_length=30,default='',unique=True)
    reference = models.CharField('Referencia',max_length=10,blank=False,unique=True,null=True)
    telephone = models.CharField('Telefono',max_length=10,default='',unique=True)
    email = models.EmailField('Correo Electronico',unique=True)
    address = models.CharField('Direccion',max_length=50,default='')

    def __str__(self):
        return self.enterprise_name


class Productos(models.Model):
    name = models.CharField('Nombre del Producto',max_length=30,unique=True)
    units = models.IntegerField('Unidades')
    enter_price = models.IntegerField('Precio de Entrada')
    exit_price = models.IntegerField('Precio de Salida')
    reference = models.CharField('Numero de Referencia',max_length=10,unique=True,blank=False,null=True,)
    Proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE,default='0',blank=False)
    Categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, default='0', blank=False)
    imagen = models.ImageField('Imagen del Producto',upload_to='img/productos/',null=True,blank=True)

    def __str__(self):
        return self.name

