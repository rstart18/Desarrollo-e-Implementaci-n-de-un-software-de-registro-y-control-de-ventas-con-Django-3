from django.db import models

# Create your models here.

class Categorias(models.Model):
    name = models.CharField(max_length=20)

class Productos(models.Model):
    name = models.CharField(max_length=20)
    units = models.IntegerField()
    enter_price = models.IntegerField()
    exit_price = models.IntegerField()