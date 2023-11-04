from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views.generic import CreateView

from .forms import USERFORM, FormUser
from .models import Usuario

# Create your views here.

def HomepageProject(request):
     return render(request, 'view/VistasPCU/vistaPrincipal.html' )

def registerUser(request):
    if request.method == 'POST':
        form = FormUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = FormUser()
    return render(request, 'registration/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        contrasena = request.POST['contrasena']
        user = authenticate(request, username=username, password=contrasena)

        if user is not None:
            login(request, user)
            # Usuario autenticado correctamente, redirige a una página de éxito.
            return HttpResponseRedirect('ruta_de_exito')
        else:
            # Autenticación fallida, muestra un mensaje de error.
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'view/VistasPCU/registration/login.html')

def CreateEvent(request):
     return render(request, 'view/VistasPCU/crearEvento.html')

def RegisterCompany(request):
     return render(request, 'view/VistasPCU/registroEmpresa.html')

def Profile(request):
     return render(request, 'view/VistasPCU/perfil.html')

def CoverImage(request):
     return render(request, 'view/VistasPCU/PantallaDeCarga.html')

def ReportEvent(request):
     return render(request, 'view/VistasPCU/ReportEvent.html')


def SelectUser(request):
    return render(request, 'view/VistasPCU/seleccionDeUsuario.html')