from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import member_required
from random import randint
from datetime import date
from Almacen.models import Productos
from Usuarios.models import User
from gestionVenta.models import Facturas,Ventas,Envios
from gestionVenta.arreglos import eliminarVaciosLista,crearDicSale
from gestionVenta.arreglos import crearDicSale

@member_required(login_url='/unauthorized/')
def sell(request):

    return  render(request, "sell.html")

@member_required(login_url='/unauthorized/')
def search_products(request):

    prd = request.GET['prd']

    if len(prd) < 30:
        productos = Productos.objects.filter(name__icontains=prd)
        return render(request, "list_product.html", {"productos": productos})
    else:
        return render(request, "list_product.html")

@member_required(login_url='/login/')
def search_clients(request):

    cedula = request.GET['search_cliente']

    if len(cedula) < 11:
        try:
            cliente = User.objects.get(cedula=cedula)
            #if cliente.groups.filter(name='Cliente').exists(): Es por si solo quiere que se le venda a los usuarios clientes
            #    return render(request, "sell.html", {"cliente": cliente})
            addCliente(request,cliente)
            return redirect('/sell/')
        except:
            print("No se encontro el cliente")
            return render(request, "sell.html")

    else:
        return render(request, "sell.html")

def fact_in_warehaouse(request):

    if request.GET['money']:
        money = int(request.GET['money'])

        if money > 0 and money >= request.session.get('fact')['total']:
            seller = request.user
            cart = request.session.get('cart')
            products = ""
            units = ""
            prices = ""
            number = len(cart)
            for key, value in cart.items():

                product_shop = Productos.objects.get(id=cart[key].get('product_id'))
                units_shop = product_shop.units
                if (int(units_shop)-int(cart[key].get('units'))) >= 0:
                    product_shop.units = int(units_shop) - int(cart[key].get('units'))
                    product_shop.save()

                    products += f"{cart[key].get('product_id')}-"
                    units += f"{cart[key].get('units')}-"
                    prices += f"{cart[key].get('price')}-"
                else:
                    messages.error(request,"no se realizo la compra debido a alguno de los elementos de tu carrito excede las existencias.")

                    request.session["cart"] = {}
                    request.session["fact"] = {}
                    request.session['cliente'] = {}
                    request.session.modified = True

                    if request.user.groups.filter(name='Cliente').exists():
                        return redirect('/shop/')
                    else:
                        return redirect('/sell/')

            fact = request.session.get('fact')
            if fact.get('discount') != None:
                discount = fact['discount']
            else:
                discount = 0
            try:
                client = request.session.get('cliente')
                total = fact['total']
                returned = money - total
                reference = randint(100000000, 999999999)

                factura = Facturas(reference=reference,
                                   number=number,
                                   products=products,
                                   units=units,
                                   prices=prices,
                                   seller=seller,
                                   discount=discount,
                                   total=total,
                                   turned=returned)
                factura.save()
                cliente = User.objects.get(cedula=client['cedula'])
                venta = Ventas(fact=factura, cliente=cliente)
                venta.save()

                request.session["cart"] = {}
                request.session["fact"] = {}
                request.session['cliente'] = {}
                request.session.modified = True

                if request.user.groups.filter(name='Cliente').exists():
                    messages.success(request, f"Se ha realizado la compra")
                    envio = Envios(no_envio=reference,status="Esperando envio",sale=venta)
                    envio.save()
                    return redirect('/shop/')

                messages.success(request, f"Deben ser devueltos {returned} COP.")
            except:
                messages.error(request, f"No se realizo la compra debido a que no asigno el cliente a vender.")
        else:

            messages.error(request, f"No se realizo la compra debido a un error en el monto.")
    else:
        messages.error(request,"No se realizo la compra debido a que no hay un monto.")
    return redirect('/sell/')

@member_required(login_url='/unauthorized/')
def box(request):
    factura = Facturas.objects.filter(date=date.today())
    total = 0
    for fact in factura:
        total = total + fact.total

    return render(request, 'box.html',{'list':factura,'total':total})

@member_required(login_url='/unauthorized/')
def view_sales(request, id_sale):
    sale = Ventas.objects.get(id=id_sale)
    products = sale.fact.products.split('-')
    products = eliminarVaciosLista(products)
    units = sale.fact.units.split('-')
    units = eliminarVaciosLista(units)
    prices = sale.fact.prices.split('-')
    prices = eliminarVaciosLista(prices)
    data = {
        'obj': sale,
        'products': crearDicSale(units,products,prices),
    }


    return render(request, 'view_sale.html', data)

@member_required(login_url='/unauthorized/')
def sales(request, pag):
    max_sales = pag * 10
    min_sales = max_sales - 10
    next = False
    prev = False

    ran = [n + 1 for n in range(min_sales, max_sales)]

    if request.method == 'POST':
        sl = request.POST.get('search')
        fact = Facturas.objects.filter(reference__icontains=sl)
        sls_query = Ventas.objects.filter(fact=fact)
        sls = sls_query[min_sales:max_sales]
        if len(sls_query[max_sales:(max_sales + 10)]) > 0:
            next = True
    else:
        sls_query = Ventas.objects.all()
        sls = sls_query[min_sales:max_sales]
        if len(sls_query[max_sales:(max_sales + 10)]) > 0:
            next = True

    if not pag == 1:
        prev = True

    # preparar los numeros de paginacion
    paginacion = [1, 2, 3, 4, 5, 6, 7, 8, 18, 28, 48]
    pags = []

    for pagina in paginacion:
        try:
            if sls_query[(pag + pagina - 1) * 10]:
                print(sls_query[(pag + pagina - 1) * 10])
                pags.append(pag + pagina)
        except:
            pass

    data = {'list': sls,
            'pags': pags,
            'pag': pag,
            'next_pag': pag + 1,
            'prev_pag': pag - 1,
            'next': next,
            'prev': prev,
            'n_sales': (pag - 1) * 10,
            }



    return render(request, 'sales.html', data)

@member_required(login_url='/unauthorized/')
def envios(request, pag):
    max_envios = pag * 10
    min_envios = max_envios - 10
    next = False
    prev = False

    ran = [n + 1 for n in range(min_envios, max_envios)]

    if request.method == 'POST':
        prvdr = request.POST.get('search')
        prvdrs_query = Envios.objects.filter(no_envio__icontains=prvdr,status='Esperando envio')
        prvdrs = prvdrs_query[min_envios:max_envios]
        if len(prvdrs_query[max_envios:(max_envios + 10)]) > 0:
            next = True
    else:
        prvdrs_query = Envios.objects.filter(status='Esperando envio')
        prvdrs = prvdrs_query[min_envios:max_envios]
        if len(prvdrs_query[max_envios:(max_envios + 10)]) > 0:
            next = True

    if not pag == 1:
        prev = True

    # preparar los numeros de paginacion
    paginacion = [1, 2, 3, 4, 5, 6, 7, 8, 18, 28, 48]
    pags = []

    for pagina in paginacion:
        try:
            if prvdrs_query[(pag + pagina - 1) * 10]:
                print(prvdrs_query[(pag + pagina - 1) * 10])
                pags.append(pag + pagina)
        except:
            pass

    data = {'list': prvdrs,
            'pags': pags,
            'pag': pag,
            'next_pag': pag + 1,
            'prev_pag': pag - 1,
            'next': next,
            'prev': prev,
            'n_envios': (pag - 1) * 10,
            }

    return render(request, 'crud/envios/viewall.html', data)

@member_required(login_url='/unauthorized/')
def processEnvio(request,id_envio):
    envio = Envios.objects.get(no_envio=id_envio)

    envio.status = "Enviado"
    envio.save()

    return redirect('/warehouse/envios/1')

def confirmEnvio(request,id_envio):
    envio = Envios.objects.get(no_envio=id_envio)

    envio.status = "Recibido"
    envio.save()

    return redirect('/purchases/')

def addCliente(request,cliente):
    request.session['cliente'] = {
        'cedula': cliente.cedula,
        'first_name': cliente.first_name,
        'last_name': cliente.last_name,
    }
    request.session.save()

def removeCliente(request):
    request.session['cliente'] = {}
    request.session.save()

# Create your views here.
