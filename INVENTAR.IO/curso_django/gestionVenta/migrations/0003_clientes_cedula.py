# Generated by Django 3.1.2 on 2020-11-16 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVenta', '0002_auto_20201109_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='cedula',
            field=models.CharField(default=1020054329, max_length=10),
            preserve_default=False,
        ),
    ]
