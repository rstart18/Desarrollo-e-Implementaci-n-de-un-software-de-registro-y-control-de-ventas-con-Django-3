from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.contrib.auth.models import Group
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
                messages.info(request, f"Has iniciado sesion : {usuario}")
                if user.groups.filter(name='Cliente').exists():
                    return redirect('/home/')
                return redirect('/dashboard/')
        else:
            messages.error(request, "Usuario o contraseña incorrecta")
            print(f"{request.POST.get('username')}:{request.POST.get('password')}")
            return redirect('/users/login/')

    form = AuthenticationForm
    return render(request, "index/login.html", {'form':form})

def logout_request(request):
    logout(request)
    messages.info(request,"Has cerrado sesion")
    return redirect('/home/')


def registration(request):

    if request.method == 'POST':
        form = CustomUserCreation(request.POST)
        if form.is_valid():
            name_user = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            cedula = form.cleaned_data.get("cedula")
            password1 = form.cleaned_data.get("password1")
            permision = request.POST.get("permision")

            usuario = User.objects.create_user(username=name_user,first_name=first_name,last_name=last_name,email=email,cedula=cedula,password=password1,is_staff=True)
            usuario.save()

            if permision == 'on':
                usuario.groups.add(Group.objects.get(name='Admin'))
            else:
                usuario.groups.add(Group.objects.get(name='Empleado'))

            messages.success(request, f"Nuevo usuario creado : {name_user}")
            #login(request,usuario)
            return redirect('/users/1')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
                return redirect('/users/1')
    form = CustomUserCreation
    return render(request,'crud/users/registration.html',{'form':form})

def registration_client(request):

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

            messages.success(request, f"Nuevo usuario creado : {name_user}")
            login(request,usuario)
            return redirect('/home/')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
                return redirect('/home/')
    form = CustomUserCreation
    return render(request,'index/register.html',{'form':form})



def users(request, pag):
    max_users = pag * 10
    min_users = max_users - 10
    next=False
    prev=False

    ran = [n+1 for n in range(min_users,max_users)]

    if request.method == 'POST':
        usr=request.POST.get('search')
        usrs_query = User.objects.filter(cedula__icontains=usr)
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
            pass

    data = {'list':usrs,
            'pags': pags,
            'pag':pag,
            'next_pag':pag+1,
            'prev_pag':pag-1,
            'next':next,
            'prev':prev,
            'n_users':(pag-1)*10,
    }

    return render(request, 'crud/users/viewall.html',data)

def user_is_exist(request):

    try:
        cedula = request.GET['cedula']


        if len(cedula) < 11 and len(cedula) > 5:

            if User.objects.filter(cedula=cedula).exists():
                usuario = User.objects.get(cedula=cedula)
                return redirect(f'/users/edit/{usuario.id}')
            return redirect('/users/registration/')
        else:
            messages.error(request, 'Campo invalido')
            return render(request, 'crud/users/user_is_exist.html')
    except:
        return render(request, 'crud/users/user_is_exist.html')



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
            return redirect('/users/1')

    return render(request,"crud/users/edit.html",{"form":form})



# Create your views here.
