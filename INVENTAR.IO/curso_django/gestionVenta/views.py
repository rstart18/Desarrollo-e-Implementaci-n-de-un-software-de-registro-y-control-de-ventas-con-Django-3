from django.shortcuts import render
from Almacen.models import Productos
from gestionVenta.models import Clientes

def sell(request):

    return  render(request, "sell.html")

def search_products(request):

    prd = request.GET['prd']

    if len(prd) < 30:
        productos = Productos.objects.filter(name__icontains=prd)
        return render(request, "list_product.html", {"productos": productos})
    else:
        return render(request, "list_product.html")

def search_clients(request):

    cedula = request.GET['search_cliente']

    if len(cedula) < 11:
        try:
            cliente = Clientes.objects.get(cedula=cedula)
            return render(request, "sell.html", {"cliente": cliente})
        except:
            print("No se encontro el cliente")
            return render(request, "sell.html")

    else:
        return render(request, "sell.html")


# Create your views here.
