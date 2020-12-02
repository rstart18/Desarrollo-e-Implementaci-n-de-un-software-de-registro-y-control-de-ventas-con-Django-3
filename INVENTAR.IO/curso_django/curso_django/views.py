from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from Almacen.models import Productos
from gestionVenta.models import Clientes

@login_required(login_url='/users/login/')
def dashboard(request):
    clientes = Clientes.objects.all()
    productos = Productos.objects.all()
    n_productos = len(productos)
    n_clientes = len(clientes)
    return render(request, "dashboard.html",{'productos':productos[:6],'n_productos':n_productos,'n_clientes':n_clientes})

def home(request):
    return render(request, 'index/index.html')

def acercade(request):
    return render(request, 'index/acercade.html')

def shop(request):
    productos = Productos.objects.all()

    return render(request, 'index/shop.html',{'productos': productos})

def login(request):
    form = AuthenticationForm

    return render(request, 'index/login.html',{'form':form})

def cuadrado(request, n):
    return HttpResponse(f"El cuadrado de {n} = {n*n}")