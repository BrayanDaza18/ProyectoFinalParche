from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .forms import Document, FormUser, FormUserCompany, UserRegister
from .models import EmpresaPersona, Persona

# Create your views here.

def HomepageProject(request):
     return render(request, 'view/VistasPCU/vistaPrincipal.html' )

def registerUser(request):
    form = FormUser()
    usuario = UserRegister()  
    
    if request.method == 'POST':
        form = FormUser(request.POST)
        # usuario = UserRegister(request.POST)
        if form.is_valid():
           data = form.save()
           data.tipousuario = 'U' 
           data.save()
        #    data = form.save() 
        #    datos =usuario.save(commit = False)
        #    datos.empresa_idEmpresa = data
        #    datos.save()
     
        return redirect('login')

    
    return render(request, 'registration/register.html', {'form': form, 'usuario': usuario})


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
    document_form = Document()  
    form = FormUserCompany()
  

    if request.method == 'POST':
        form = FormUserCompany(request.POST)
        document_form = Document(request.POST, request.FILES) 

        if form.is_valid() and document_form.is_valid():
            data = form.save() 
            data.tipousuario = 'E' 
            data.save()
            datos = document_form.save(commit=False)
            datos.empresa_idempresa = data
            datos.save()

        else:
          print("Errores en el formulario FormUserCompany:", form.errors)
          print("Errores en el formulario Document:", document_form.errors)
        return redirect('login')

    return render(request, 'registration/registroEmpresa.html', {'document': document_form, 'form': form})

def MostrarEvento(request):
    return render(request, 'view/VistasPCU/mostrarEventos.html')

def Profile(request):
     return render(request, 'view/VistasPCU/perfil.html')

def CoverImage(request):
     return render(request, 'view/VistasPCU/PantallaDeCarga.html')

def ReportEvent(request):
     return render(request, 'view/VistasPCU/ReportEvent.html')


def SelectUser(request):
    return render(request, 'view/VistasPCU/seleccionDeUsuario.html')