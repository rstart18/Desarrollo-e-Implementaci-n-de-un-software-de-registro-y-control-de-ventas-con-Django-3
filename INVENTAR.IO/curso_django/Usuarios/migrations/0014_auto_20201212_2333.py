# Generated by Django 3.1.2 on 2020-12-13 04:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0013_auto_20201212_2229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditcards',
            name='due_date',
        ),
        migrations.AddField(
            model_name='creditcards',
            name='año_de_vencimiento',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='creditcards',
            name='mes_de_vencimiento',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)]),
        ),
    ]