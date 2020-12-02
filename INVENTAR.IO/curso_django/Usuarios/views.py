from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from Usuarios.forms import CustomUserCreation,CustomUserEdit


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contrasena = form.cleaned_data.get('password')

            user = authenticate(username=usuario,password=contrasena)

            if user is not None:
                login(request, user)
                messages.info(request,f"Has iniciado sesion : {usuario}")
                return redirect('/dashboard/')
        else:
            messages.error(request, "Usuario o contraseña incorrecta")
            print(f"{request.POST.get('username')}:{request.POST.get('password')}")
            return redirect('/users/login/')

    form = AuthenticationForm
    return render(request, "users/login.html", {'form':form})

def logout_request(request):
    logout(request)
    messages.info(request,"Has cerrado sesion")
    return redirect('/dashboard/')


def registration(request):

    if request.method == 'POST':
        form = CustomUserCreation(request.POST)
        if form.is_valid():
            usuario = form.save()
            name_user = form.cleaned_data.get("username")
            messages.success(request, f"Nuevo usuario creado : {name_user}")
            #login(request,usuario)
            return redirect('/dashboard/')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
                return redirect('/dashboard/')
    form = CustomUserCreation
    return render(request,'crud/registration.html',{'form':form})

def users(request, pag):
    max_users = pag * 10
    min_users = max_users - 10
    next=False
    prev=False

    if request.method == 'POST':
        usr=request.POST.get('search')
        usrs_query = User.objects.filter(username__icontains=usr)
        usrs = usrs_query[min_users:max_users]
        if len(usrs_query[max_users:(max_users + 10)]) > 0:
            next = True
    else:
        usrs_query = User.objects.all()
        usrs = usrs_query[min_users:max_users]
        if len(usrs_query[max_users:(max_users + 10)]) > 0:
            next = True

    if not pag == 1:
        prev = True

    #preparar los numeros de paginacion
    paginacion = [1,2,3,4,5,6,7,8,18,28,48]
    pags = []

    for pagina in paginacion:
        try:
            if usrs_query[(pag+pagina-1)*10]:
                print(usrs_query[(pag+pagina-1)*10])
                pags.append(pag+pagina)
        except:
            print(f"La pagina no existe.")

    data = {'list':usrs,
            'verbose_name':'Usuario',
            'verbose_name_plural':'Usuarios',
            'template_name':'users',
            'pags': pags,
            'pag':pag,
            'next_pag':pag+1,
            'prev_pag':pag-1,
            'next':next,
            'prev':prev,
    }

    return render(request, 'crud/viewall.html',data)

def delete(request,user_id):

    usrs = User.objects.filter(id=user_id)
    usrs.delete()

    return redirect('/users/1')

def edit(request, user_id):

    user_instance = User.objects.get(id=user_id)
    form = CustomUserEdit(instance=user_instance)

    if request.method == 'POST':
        form = CustomUserEdit(request.POST,instance=user_instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            messages.success(request, f"El usuario {user_instance.username} ha sido editado con exito!")
            return redirect('/dashboard/')

    return render(request,"crud/edit.html",{"form":form})



# Create your views here.
