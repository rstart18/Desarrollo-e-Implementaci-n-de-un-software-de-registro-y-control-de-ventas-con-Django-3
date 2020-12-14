from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import member_required
from Almacen.forms import *
from Almacen.models import Productos,Proveedores,Categorias
from Usuarios.forms import *

@member_required(login_url='/unauthorized/')
def products(request, pag):
    max_products = pag * 10
    min_products = max_products - 10
    next = False
    prev = False

    ran = [n + 1 for n in range(min_products, max_products)]

    if request.method == 'POST':
        prdct = request.POST.get('search')
        prdcts_query = Productos.objects.filter(reference__icontains=prdct)
        prdcts = prdcts_query[min_products:max_products]
        if len(prdcts_query[max_products:(max_products + 10)]) > 0:
            next = True
    else:
        prdcts_query = Productos.objects.all()
        prdcts = prdcts_query[min_products:max_products]
        if len(prdcts_query[max_products:(max_products + 10)]) > 0:
            next = True

    if not pag == 1:
        prev = True

    # preparar los numeros de paginacion
    paginacion = [1, 2, 3, 4, 5, 6, 7, 8, 18, 28, 48]
    pags = []

    for pagina in paginacion:
        try:
            if prdcts_query[(pag + pagina - 1) * 10]:
                print(prdcts_query[(pag + pagina - 1) * 10])
                pags.append(pag + pagina)
        except:
            pass

    data = {'list': prdcts,
            'pags': pags,
            'pag': pag,
            'next_pag': pag + 1,
            'prev_pag': pag - 1,
            'next': next,
            'prev': prev,
            'n_products': (pag - 1) * 10,
            }

    return render(request, 'crud/products/viewall.html', data)

@member_required(login_url='/unauthorized/')
def inventory(request, pag):
    max_products = pag * 10
    min_products = max_products - 10
    next = False
    prev = False

    ran = [n + 1 for n in range(min_products, max_products)]

    if request.method == 'POST':
        prdct = request.POST.get('search')
        prdcts_query = Productos.objects.filter(reference__icontains=prdct)
        prdcts = prdcts_query[min_products:max_products]
        if len(prdcts_query[max_products:(max_products + 10)]) > 0:
            next = True
    else:
        prdcts_query = Productos.objects.all()
        prdcts = prdcts_query[min_products:max_products]
        if len(prdcts_query[max_products:(max_products + 10)]) > 0:
            next = True

    if not pag == 1:
        prev = True

    # preparar los numeros de paginacion
    paginacion = [1, 2, 3, 4, 5, 6, 7, 8, 18, 28, 48]
    pags = []

    for pagina in paginacion:
        try:
            if prdcts_query[(pag + pagina - 1) * 10]:
                print(prdcts_query[(pag + pagina - 1) * 10])
                pags.append(pag + pagina)
        except:
            pass

    data = {'list': prdcts,
            'pags': pags,
            'pag': pag,
            'next_pag': pag + 1,
            'prev_pag': pag - 1,
            'next': next,
            'prev': prev,
            'n_products': (pag - 1) * 10,
            }

    return render(request, 'crud/products/inventory.html', data)

@member_required(login_url='/unauthorized/')
def catering(request):
    if request.method == 'POST':
        form = ProductCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/warehouse/products/1')
        else:
            messages.error(request, "Algun campo no es valido")
            return redirect('/warehouse/products/catering/')


    form = ProductCreationForm
    return render(request,'crud/products/catering.html', {'form':form})

@member_required(login_url='/unauthorized/')
def supply(request, product_id):

    product_instance = Productos.objects.get(id=product_id)
    form = SupplyForm(instance=product_instance)

    if request.method == 'POST':
        form = SupplyForm(request.POST,instance=product_instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            messages.success(request, f"El producto {product_instance.name} ha sido editado con exito!")
            return redirect('/warehouse/products/1')

    return render(request,"crud/products/supply.html",{"form":form})

@member_required(login_url='/unauthorized/')
def search_supply(request):

    try:
        reference = request.GET['reference']

        if len(reference) < 11:

            if Productos.objects.filter(reference=reference).exists():
                producto = Productos.objects.get(reference=reference)
                print(producto.id)
                return redirect(f'/warehouse/products/supply/{producto.id}')
            else:
                return redirect('/warehouse/products/1')
        else:
            messages.error(request, 'Campo invalido')
            return render(request, 'crud/products/search_supply.html')
    except:
        return render(request, 'crud/products/search_supply.html')

@member_required(login_url='/unauthorized/')
def edit_product(request, product_id):

    product_instance = Productos.objects.get(id=product_id)
    form = ProductEditForm(instance=product_instance)

    if request.method == 'POST':
        form = ProductEditForm(request.POST,instance=product_instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            messages.success(request, f"El producto {product_instance.name} ha sido editado con exito!")
            return redirect('/warehouse/products/1')

    return render(request,"crud/products/edit.html",{"form":form})

@member_required(login_url='/unauthorized/')
def delete_product(request,product_id):

    prdct = Productos.objects.filter(id=product_id)
    prdct.delete()

    return redirect('/warehouse/products/1')

@member_required(login_url='/unauthorized/')
def products_is_exist(request):

    try:
        reference = request.GET['reference']

        if len(reference) < 11:

            if Productos.objects.filter(reference=reference).exists():
                return redirect(f'/warehouse/products/supply')
            else:
                return redirect('/warehouse/products/catering/')
        else:
            messages.error(request, 'Campo invalido')
            return render(request, 'crud/products/products_is_exist.html')
    except:
        return render(request, 'crud/products/products_is_exist.html')



    '''
    -------------- PROVEEDORES ---------------
    '''

@member_required(login_url='/unauthorized/')
def providers(request, pag):
    max_providers = pag * 10
    min_providers = max_providers - 10
    next = False
    prev = False

    ran = [n + 1 for n in range(min_providers, max_providers)]

    if request.method == 'POST':
        prvdr = request.POST.get('search')
        prvdrs_query = Proveedores.objects.filter(enterprise_name__icontains=prvdr)
        prvdrs = prvdrs_query[min_providers:max_providers]
        if len(prvdrs_query[max_providers:(max_providers + 10)]) > 0:
            next = True
    else:
        prvdrs_query = Proveedores.objects.all()
        prvdrs = prvdrs_query[min_providers:max_providers]
        if len(prvdrs_query[max_providers:(max_providers + 10)]) > 0:
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
            'n_providers': (pag - 1) * 10,
            }

    return render(request, 'crud/providers/viewall.html', data)

@member_required(login_url='/unauthorized/')
def register_provider(request):
    if request.method == 'POST':
        form = ProviderCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Se ha registrado el proveedor {form.cleaned_data.get("enterprise_name")}')
        else:
            messages.error(request, "Algun campo no es valido")
        return redirect('/warehouse/providers/register')

    form = ProviderCreationForm()
    return render(request,'crud/providers/registration.html',{'form':form})

@member_required(login_url='/unauthorized/')
def edit_provider(request, provider_id):

    provider_instance = Proveedores.objects.get(id=provider_id)
    form = ProviderEditForm(instance=provider_instance)

    if request.method == 'POST':
        form = ProviderEditForm(request.POST,instance=provider_instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            messages.success(request, f"El proveedor {provider_instance.enterprise_name} ha sido editado con exito!")
            return redirect('/warehouse/providers/1')

    return render(request,"crud/providers/edit.html",{"form":form})

@member_required(login_url='/unauthorized/')
def delete_provider(request,provider_id):

    prvdr = Proveedores.objects.filter(id=provider_id)
    prvdr.delete()

    return redirect('/warehouse/providers/1')

@member_required(login_url='/unauthorized/')
def providers_is_exist(request):

    try:
        reference = request.GET['reference']

        if len(reference) < 11:

            if Proveedores.objects.filter(reference=reference).exists():
                provider = Proveedores.objects.get(reference=reference)
                return redirect(f'/warehouse/providers/edit/{provider.id}')
            else:
                return redirect('/warehouse/providers/register')
        else:
            messages.error(request, 'Campo invalido')
            return render(request, 'crud/providers/providers_is_exist.html')
    except:
        return render(request, 'crud/providers/providers_is_exist.html')

    '''
    -------------- CATEGORIAS ----------------
    '''

@member_required(login_url='/unauthorized/')
def categorys(request, pag):
    max_categorys = pag * 10
    min_categorys = max_categorys - 10
    next = False
    prev = False

    ran = [n + 1 for n in range(min_categorys, max_categorys)]

    if request.method == 'POST':
        ctgr = request.POST.get('search')
        ctgrs_query = Categorias.objects.filter(name__icontains=ctgr)
        ctgrs = ctgrs_query[min_categorys:max_categorys]
        if len(ctgrs_query[max_categorys:(max_categorys + 10)]) > 0:
            next = True
    else:
        ctgrs_query = Categorias.objects.all()
        ctgrs = ctgrs_query[min_categorys:max_categorys]
        if len(ctgrs_query[max_categorys:(max_categorys + 10)]) > 0:
            next = True

    if not pag == 1:
        prev = True

    # preparar los numeros de paginacion
    paginacion = [1, 2, 3, 4, 5, 6, 7, 8, 18, 28, 48]
    pags = []

    for pagina in paginacion:
        try:
            if ctgrs_query[(pag + pagina - 1) * 10]:
                print(ctgrs_query[(pag + pagina - 1) * 10])
                pags.append(pag + pagina)
        except:
            pass

    data = {'list': ctgrs,
            'pags': pags,
            'pag': pag,
            'next_pag': pag + 1,
            'prev_pag': pag - 1,
            'next': next,
            'prev': prev,
            'n_categorys': (pag - 1) * 10,
            }

    return render(request, 'crud/categorys/viewall.html', data)

@member_required(login_url='/unauthorized/')
def register_category(request):
    if request.method == 'POST':
        form = CategoryCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Se ha registrado la categoria {form.cleaned_data.get("name")}')
        else:
            messages.error(request, "Algun campo no es valido")

        return redirect('/warehouse/categorys/register')

    form = CategoryCreationForm()
    return render(request,'crud/categorys/registration.html',{'form':form})

@member_required(login_url='/unauthorized/')
def edit_category(request, category_id):

    category_instance = Categorias.objects.get(id=category_id)
    form = CategoryEditForm(instance=category_instance)

    if request.method == 'POST':
        form = CategoryEditForm(request.POST,instance=category_instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            messages.success(request, f"La categoria {category_instance.name} ha sido editado con exito!")
            return redirect('/warehouse/categorys/1')

    return render(request,"crud/categorys/edit.html",{"form":form})

@member_required(login_url='/unauthorized/')
def delete_category(request,category_id):

    ctgry = Categorias.objects.filter(id=category_id)
    ctgry.delete()

    return redirect('/warehouse/categorys/1')

@member_required(login_url='/unauthorized/')
def categorys_is_exist(request):

    try:
        reference = request.GET['reference']

        if len(reference) < 11:

            if Categorias.objects.filter(reference=reference).exists():
                category = Categorias.objects.get(reference=reference)
                return redirect(f'/warehouse/categorys/edit/{category.id}')
            else:
                return redirect('/warehouse/categorys/register')
        else:
            messages.error(request, 'Campo invalido')
            return render(request, 'crud/categorys/categorys_is_exist.html')
    except:
        return render(request, 'crud/categorys/categorys_is_exist.html')

'''
    -------------- CLIENTES ----------------
    '''

@member_required(login_url='/unauthorized/')
def clients(request, pag):
    max_clients = pag * 10
    min_clients = max_clients - 10
    next = False
    prev = False

    ran = [n + 1 for n in range(min_clients, max_clients)]

    if request.method == 'POST':
        clnt = request.POST.get('search')
        clnts_query = User.objects.filter(cedula__icontains=clnt,groups__name='Cliente')
        clnts = clnts_query[min_clients:max_clients]
        if len(clnts_query[max_clients:(max_clients + 10)]) > 0:
            next = True
    else:
        clnts_query = User.objects.filter(groups__name='Cliente')
        clnts = clnts_query[min_clients:max_clients]
        if len(clnts_query[max_clients:(max_clients + 10)]) > 0:
            next = True

    if not pag == 1:
        prev = True

    # preparar los numeros de paginacion
    paginacion = [1, 2, 3, 4, 5, 6, 7, 8, 18, 28, 48]
    pags = []

    for pagina in paginacion:
        try:
            if clnts_query[(pag + pagina - 1) * 10]:
                print(clnts_query[(pag + pagina - 1) * 10])
                pags.append(pag + pagina)
        except:
            pass

    data = {'list': clnts,
            'pags': pags,
            'pag': pag,
            'next_pag': pag + 1,
            'prev_pag': pag - 1,
            'next': next,
            'prev': prev,
            'n_clients': (pag - 1) * 10,
            }

    return render(request, 'crud/clients/viewall.html', data)

@member_required(login_url='/unauthorized/')
def delete_clients(request,client_id):

    clnt = Categorias.objects.filter(id=client_id)
    clnt.delete()

    return redirect('/warehouse/clietns/1')

@member_required(login_url='/unauthorized/')
def clients_is_exist(request):

    try:
        reference = request.GET['reference']

        if len(reference) < 11:

            if User.objects.filter(cedula=reference,groups__name='Cliente').exists():
                cliente = User.objects.get(cedula=reference,groups__name='Cliente')
                return redirect(f'/warehouse/clients/edit/{cliente.id}')
            else:
                return redirect('/warehouse/clients/register')
        else:
            messages.error(request, 'Campo invalido')
            return render(request, 'crud/clients/clients_is_exist.html')
    except:
        return render(request, 'crud/clients/clients_is_exist.html')

@member_required(login_url='/unauthorized/')
def register_client(request):

    if request.method == 'POST':
        form = CustomUserCreation(request.POST)
        if form.is_valid():
            name_user = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            cedula = form.cleaned_data.get("cedula")
            password1 = form.cleaned_data.get("password1")

            usuario = User.objects.create_user(username=name_user,first_name=first_name,last_name=last_name,email=email,cedula=cedula,password=password1,is_staff=True)
            usuario.save()

            usuario.groups.add(Group.objects.get(name='Cliente'))

            messages.success(request, f"Nuevo usuario creado : {first_name} {last_name}")
            return redirect('/warehouse/clients/1')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
                return redirect('/warehouse/clients/register')
    form = CustomUserCreation
    return render(request,'crud/clients/registration.html',{'form':form})

@member_required(login_url='/unauthorized/')
def edit_client(request, client_id):

    user_instance = User.objects.get(id=client_id)
    form = CustomUserEdit(instance=user_instance)

    if request.method == 'POST':
        form = CustomUserEdit(request.POST,instance=user_instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            messages.success(request, f"El cliente {user_instance.first_name} {user_instance.last_name} ha sido editado con exito!")
            return redirect('warehouse/clients/1')

    return render(request,"crud/clients/edit.html",{"form":form})

# Create your views here.
