# Generated by Django 3.1.2 on 2020-12-12 05:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVenta', '0015_auto_20201212_0020'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturas',
            name='turned',
            field=models.IntegerField(default=0, verbose_name='Vueltos'),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 12, 0, 41, 23, 911199), verbose_name='Fecha'),
        ),
    ]
