from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class User(AbstractUser):
    cedula = models.IntegerField(
        validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(100000)
        ],
        unique=True,
        blank=False,
        null=True,
    )
    def __str__(self):
        return self.username


class CreditCards(models.Model):
    cc = models.CharField('Numero de tarjeta',max_length=16,blank=False,null=False,default='')
    mes_de_vencimiento = models.IntegerField(validators=[MaxValueValidator(12),MinValueValidator(1)],blank=False,null=False,default=0)
    año_de_vencimiento = models.IntegerField(validators=[MaxValueValidator(99), MinValueValidator(20)], blank=False,null=False, default=0)
    ccv = models.IntegerField(validators=[MaxValueValidator(999), MinValueValidator(111)], blank=False,null=False, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='0', blank=False)

    def __str__(self):
        return f"{self.cc} - {self.user.username}"



# Create your models here.
