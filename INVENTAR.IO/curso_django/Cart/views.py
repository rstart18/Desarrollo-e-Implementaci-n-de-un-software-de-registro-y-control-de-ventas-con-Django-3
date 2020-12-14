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
        if units == None:
            cart.add(product=product, units=1)
        else:
            if int(units) > 0:
                cart.add(product=product, units=units)
            else:
                messages.error(request,"Unidades de producto no validas")
                return redirect('/dashboard/')
    if request.user.groups.filter(name='Cliente').exists():
        messages.success(request, f"Se ha añadido {product.name} al carrito!")
        return redirect('/shop/')
    return redirect('/sell/')

def remove_product(request):


    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = Cart(request)
        product = Productos.objects.get(id=product_id)
        cart.remove(product)

    if request.user.groups.filter(name='Cliente').exists():
        messages.error(request, f"Se ha eliminado {product.name} del carrito")
        return redirect('/cart/')

    return redirect('/sell/')

def discount_cart(request):
    if request.method == 'POST':
        discount = request.POST.get('discount')
        cart = Cart(request)
        if int(discount) >= 0 :
            cart.discount(discount)
        else:
            messages.error(request,"Porcentaje de descuento no valido")
            return redirect('/dashboard/')
    return redirect('/sell/')

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    if request.user.groups.filter(name='Cliente').exists():
        return redirect('/shop/')
    return redirect('/sell/')