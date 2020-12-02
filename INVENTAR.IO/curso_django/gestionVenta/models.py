from django.db import models

# Create your models here.

class Clientes(models.Model):
    name=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    cedula = models.CharField(max_length=10,blank=False)
    tlf=models.CharField(max_length=10)
    email=models.EmailField()

class Proveedores(models.Model):
    name = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    tlf = models.CharField(max_length=10)
    email = models.EmailField()
    direccion = models.CharField(max_length=30)

class Ventas(models.Model):
    factura = models.IntegerField()
    id_cliente = models.IntegerField()