from django.shortcuts import render,redirect
from django.contrib import messages
from Almacen.models import Productos
from .Cart import Cart

def add_product(request):

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = Cart(request)
        product = Productos.objects.get(id=product_id)
        units = request.POST.get('product_units')
        if int(units) > 0:
            cart.add(product=product, units=units)
        else:
            messages.error(request,"Unidades de producto no validas")
            return redirect('/dashboard/')
    return redirect('/sell/')

def remove_product(request):


    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = Cart(request)
        product = Productos.objects.get(id=product_id)
        cart.remove(product)

    return redirect('/sell/')

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('/sell/')