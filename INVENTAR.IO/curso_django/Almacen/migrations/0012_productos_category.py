# Generated by Django 3.1.2 on 2020-12-07 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Almacen', '0011_productos_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='category',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='Almacen.categorias'),
        ),
    ]
