# Generated by Django 3.1.2 on 2020-11-22 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Almacen', '0003_auto_20201121_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='curso_django/uploads/img/productos/', verbose_name='Imagen del Producto'),
        ),
    ]
