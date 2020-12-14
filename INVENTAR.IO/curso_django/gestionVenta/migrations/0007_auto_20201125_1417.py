# Generated by Django 3.1.2 on 2020-11-25 19:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVenta', '0006_auto_20201125_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='cedula',
            field=models.IntegerField(max_length=10, unique=True, validators=[django.core.validators.MaxValueValidator(9999999999), django.core.validators.MinValueValidator(100000)]),
        ),
    ]
