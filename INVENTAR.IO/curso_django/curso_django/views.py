from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import member_required
from Almacen.models import Productos,Categorias,Proveedores
from gestionVenta.models import Ventas,Envios,Facturas
from Usuarios.models import User,CreditCards
from Usuarios.forms import AddCreditCard
from gestionVenta.arreglos import eliminarVaciosLista,crearDicSale
from django.http import HttpResponse



@member_required(login_url='/unauthorized/')
def dashboard(request):
    clientes = User.objects.filter(groups__name__in=['Cliente'])
    productos = Productos.objects.all()
    categorias = Categorias.objects.all()
    proveedores = Proveedores.objects.all()
    n_productos = len(productos)
    n_clientes = len(clientes)
    n_categorias = len(categorias)
    n_proveedores = len(proveedores)
    return render(request, "dashboard.html",{'productos':productos[:6],'n_productos':n_productos,'n_clientes':n_clientes,'n_proveedores':n_proveedores,'n_categorias':n_categorias})

def home(request):
    return render(request, 'index/index.html')


def acercade(request):
    return render(request, 'index/acercade.html')

def profile(request):
    return render(request, 'index/profile.html')

def shop(request):
    productos = Productos.objects.all()

    return render(request, 'index/shop.html',{'productos': productos})

def cart(request):
    return render(request, 'index/cart.html')

@member_required(login_url='/unauthorized/')
def report_inventory(request):
    return render(request, 'report_inventory.html')

@member_required(login_url='/unauthorized/')
def view_report_inventory(request):
    list = Productos.objects.all()
    return render(request, 'view_report_inventory.html',  {'list':list})

@member_required(login_url='/unauthorized/')
def report_sales(request):
    return render(request, 'report_sales.html')

@member_required(login_url='/unauthorized/')
def view_report_sales(request):
    list = Ventas.objects.all()
    return render(request, 'view_report_sales.html',  {'list':list})

def view_purchases(request, id_purchase):
    envio = Envios.objects.get(no_envio=id_purchase)
    fact = Facturas.objects.get(reference=id_purchase)
    sale = Ventas.objects.get(fact=fact)
    products = sale.fact.products.split('-')
    products = eliminarVaciosLista(products)
    units = sale.fact.units.split('-')
    units = eliminarVaciosLista(units)
    prices = sale.fact.prices.split('-')
    prices = eliminarVaciosLista(prices)
    data = {
        'obj': sale,
        'products': crearDicSale(units,products,prices),
        'envio':envio,
    }


    return render(request, 'index/view_purchases.html', data)

def purchases(request):

    try:
        ventas = Ventas.objects.filter(cliente=request.user)
        envios = []
        for venta in ventas:
            envios.append(Envios.objects.get(sale=venta))

        return render(request, 'index/purchases.html', {'envios': envios})
    except:
        return render(request, 'index/purchases.html')

def confirmCreditCard(request):
    try:
        cc = CreditCards.objects.get(user=request.user)
        if cc:
            request.session['cliente'] = {
                'cedula': request.user.cedula,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }
            request.session.save()
            fact = request.session.get('fact')
            return redirect(f'/sell/fact?money={fact["total"]}')
    except:
        messages.info(request, "Añade una tarjeta de credito antes de hacer la compra")
        return redirect('/addCreditCard/')

def addCreditCard(request):
    if request.method == 'POST':
        form = AddCreditCard(request.POST)
        if form.is_valid():
            cc = form.cleaned_data.get("cc")
            mes_de_vencimiento = form.cleaned_data.get("mes_de_vencimiento")
            año_de_vencimiento = form.cleaned_data.get("año_de_vencimiento")
            ccv = form.cleaned_data.get("ccv")
            user = request.user

            creditcard = CreditCards(cc=cc,
                                     mes_de_vencimiento=mes_de_vencimiento,
                                     año_de_vencimiento=año_de_vencimiento,
                                     ccv=ccv
                                     ,user=user
                                     )

            creditcard.save()

            messages.success(request, f'Ya has registrado tu tarjeta de credito')
        else:
            messages.error(request, "Algun campo no es valido")

        request.session['cliente'] = {
            'cedula': request.user.cedula,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        request.session.save()
        fact = request.session.get('fact')
        return redirect(f'/sell/fact?money={fact["total"]}')

    form = AddCreditCard
    return render(request, 'index/creditcard/add.html',{'form':form})

def unathorized(request):

    data = 'Upps : No tienes permisos para realizar esta accion'

    return render(request, 'response.html',{'response':data})

def cuadrado(request, n):
    return HttpResponse(f"El cuadrado de {n} = {n*n}")
