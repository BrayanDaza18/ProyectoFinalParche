from datetime import datetime
from pyexpat.errors import messages
from smtplib import SMTPException
import folium
from django.conf import settings
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template

from .forms import (CreateEventos, Document, FormCompanyUpdate, FormUser,
                    FormUserCompany, FormUserUpdate, UserRegister)
from .models import Actividad, EmpresaPersona, Persona

# Create your views here.

def HomepageProject(request):
     return render(request, 'view/VistasPCU/vistaPrincipal.html')

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
        correo = request.POST.get('correo')
        usuario = request.POST.get('usuario')
        now = datetime.now()
        fecha_hora_actual = now.strftime("%Y-%m-%d %H:%M:%S")

        send_email(correo, usuario, fecha_hora_actual)
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
    activity = CreateEventos()
    if request.method == 'POST':
        activity = CreateEventos(request.POST, request.FILES)
        if activity.is_valid():
            usuario = activity.save(commit=False)
            usuario.empresa_idempresa = request.user
            usuario.save()
        else:
            print("Errores en el formulario CreateEventos:", activity.errors)

        return redirect('vistaPrincipal')
    
    return render(request, 'view/VistasPCU/crearEvento.html', {'activity': activity})



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
       
            usuario = request.POST.get('usuario')
            correo = request.POST.get('correo')
            nombreempresa = request.POST.get('nombreempresa')
            now = datetime.now()
            fecha_hora_actual = now.strftime("%Y-%m-%d %H:%M:%S")
            
            send_email_empresa(usuario, correo, nombreempresa, fecha_hora_actual)

        else:
          print("Errores en el formulario FormUserCompany:", form.errors)
          print("Errores en el formulario Document:", document_form.errors)
        return redirect('login')

    return render(request, 'registration/registroEmpresa.html', {'document': document_form, 'form': form})


def MostrarEvento(request):
    query = request.GET.get('q', '')  # Obtén el parámetro de búsqueda del nombre de la actividad
    tipo_actividad = request.GET.get('tipo_actividad', '')  # Corrige el nombre del parámetro

    # Filtra los eventos según los parámetros de búsqueda
    eventos = Actividad.objects.all()
    if query:
        eventos = eventos.filter(nombreactividad__icontains=query)
    if tipo_actividad:
        eventos = eventos.filter(tipoactividad=tipo_actividad)

    # Obtén las opciones de tipo de actividad del modelo
    tipo_actividad_choices = Actividad.deporte

    context = {'data': eventos, 'tipo_actividad_choices': tipo_actividad_choices}
    return render(request, 'view/VistasPCU/mostrarEventos.html', context)


def Profile(request):
    usuario = request.user
    form = Actividad.objects.filter(empresa_idempresa=usuario)
    actividad = EmpresaPersona.objects.all()
    print(form)
      
    return render(request, 'view/VistasPCU/perfil.html', {'data': form, 'actividad': actividad})


def CoverImage(request):
     return render(request, 'view/VistasPCU/PantallaDeCarga.html')

def ReportEvent(request):
     return render(request, 'view/VistasPCU/ReportEvent.html')


def SelectUser(request):
    return render(request, 'view/VistasPCU/seleccionDeUsuario.html')


def eventForUser(request):
    users = request.user
    data = Actividad.objects.filter(empresa_idempresa = users)
    print(data)
    return render(request, 'view/VistasPCU/viewCreateEventForUser.html',{'data': data})


def viewEventoELI(request, idactividad):
    data = Actividad.objects.get(idactividad=idactividad)
    data.delete()

    return redirect('eventUser')

def UpdateEvent(request, idactividad):
    event = Actividad.objects.get(idactividad=idactividad)

    form = CreateEventos(request.POST  or None, request.FILES  or None, instance=event)

    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('eventUser')
    
    else:
        print(form.errors)

        
    return render(request, 'view/VistasPCU/UpdateEvent.html', {'form': form})


def UpdateUser(request, idregistro,tipousuario):
    # usuario = request.user
    activity = EmpresaPersona.objects.get(idregistro=idregistro, tipousuario=tipousuario)
    # post = get_object_or_404(activity, pk=idregistro)
    form = FormUserUpdate(request.POST or None, request.FILES or None, instance= activity )
 
   
    if form.is_valid() and request.method == 'POST':
        form.save()
        update_session_auth_hash(request, form)
        return redirect('profile')
    else:
        print(form.errors)

    return render(request, 'view/VistasPCU/UpdateUser.html',  {'form': form})

    
def UpdateUserCompany(request, idregistro, tipousuario):
    # usuario = request.user
    activity = EmpresaPersona.objects.get(idregistro=idregistro, tipousuario=tipousuario)
    # post = get_object_or_404(activity, pk=idregistro)
    form = FormCompanyUpdate(request.POST or None, request.FILES or None, instance= activity )
 
   
    if form.is_valid() and request.method == 'POST':
        form.save()
        update_session_auth_hash(request, form)
        return redirect('profile')
    else:
        print(form.errors)

    return render(request, 'view/VistasPCU/UpdateUser.html',  {'form': form})



def send_email(correo, usuario, fecha_hora_actual):
    try:
        context = {'correo': correo, 'usuario': usuario, 'current_datetime': fecha_hora_actual}
        template = get_template('correo.html')
        content = template.render(context)
        print(correo)
        print(usuario)

        email = EmailMultiAlternatives(
            'Registro exitoso en Parche',  # Título
            'Probando app parche',  # Descripción
            settings.EMAIL_HOST_USER,  # Quién envía el correo
            [correo]
        )

        email.attach_alternative(content, 'text/html')
        email.send()

    except (ValidationError, SMTPException) as e:
        print(f"Error al enviar correo: {e}")


def send_email_empresa(usuario, correo, nombreempresa, fecha_hora_actual):
    try:
        context = {'usuario': usuario, 'correo': correo, 'nombreempresa': nombreempresa, 'current_datetime': fecha_hora_actual}
        template = get_template('correo_empresa.html')
        content = template.render(context)
        print(usuario)
        print(correo)
        print(nombreempresa)

        email = EmailMultiAlternatives(
            'Registro exitoso en Parche',  # Título
            'Probando app parche',  # Descripción
            settings.EMAIL_HOST_USER,  # Quién envía el correo
            [correo]
        )

        email.attach_alternative(content, 'text/html')
        email.send()

    except (ValidationError, SMTPException) as e:
        print(f"Error al enviar correo: {e}")
