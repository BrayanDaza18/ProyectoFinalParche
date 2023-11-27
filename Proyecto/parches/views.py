from datetime import datetime
from smtplib import SMTPException
from folium import Marker
import folium
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from folium import Marker

from .forms import (CreateEventos, Document, FormCompanyUpdate, FormUser,
                    FormUserCompany, FormUserUpdate, UserRegister,
                    comentarioUserform, joinEventP)
from .models import (Actividad, EmpresaPersona, Persona, Realizacion,
                     comentarioUSer)

from django.contrib import messages
# from .forms import UserReportForm
from django.core.mail import send_mail

from django.contrib.auth import get_user_model
from django.template.loader import get_template


# REPORTAR
# from .models import Usuario 

# Create your views here.


# def home(request):
#     initialMap = folium.Map(location=[2.9349676,-75.2914166], zoom_start= 13)
#     context = {'map': initialMap._repr_html_()}
#     return render (request, 'view/folium.html', context)



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
        send_report_email(usuario,request)
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
    query = request.GET.get('q', '')
    tipo_actividad = request.GET.get('tipo_actividad', '') 
    form = EmpresaPersona.objects.all()
    eventos = Actividad.objects.all()
    if query:
        eventos = eventos.filter(nombreactividad__icontains=query)
    if tipo_actividad:
        eventos = eventos.filter(tipoactividad=tipo_actividad)

    tipo_actividad_choices = Actividad.deporte

    maps = []
    for evento in eventos:
        map = folium.Map(location=[evento.latitud, evento.longitud], zoom_start=13)
        folium.Marker(
            location=[evento.latitud, evento.longitud],
            popup=f"{evento.nombreactividad}"
        ).add_to(map)
        maps.append({
            "map": map._repr_html_(),
            "idactividad": evento.pk
        })

    context = {'data': eventos,'form':form, 'tipo_actividad_choices': tipo_actividad_choices, 'maps': maps}
    return render(request, 'view/VistasPCU/mostrarEventos.html', context)



def DetallesEvento(request, idactividad):
    evento = get_object_or_404(Actividad, idactividad=idactividad)

    mapa = folium.Map(location=[evento.latitud, evento.longitud], zoom_start=13)
    folium.Marker(
        location=[evento.latitud, evento.longitud],
        popup=f"{evento.nombreactividad} - Coordenadas: {evento.latitud}, {evento.longitud}"
    ).add_to(mapa)

    mapa_html = mapa._repr_html_()

    return render(request, 'view/VistasPCU/detalles_evento.html', {'evento': evento, 'mapa_html': mapa_html})


def Profile(request):
    usuario = request.user
    form = Actividad.objects.filter(empresa_idempresa=usuario)
    comment = comentarioUSer.objects.filter(author = usuario).order_by('created_on')
    actividad = EmpresaPersona.objects.all()

    if request.method == 'POST':
       comment = comentarioUserform(request.POST)

       if comment.is_valid():
            commentUser = comment.save(commit=False)
            commentUser.author = request.user
            commentUser.receptor = request.user
            commentUser.save()
            return redirect('profile')
      
    return render(request, 'view/VistasPCU/perfil.html', {'data': form, 'actividad': actividad, 'comment': comment})


def CoverImage(request):
     return render(request, 'view/VistasPCU/PantallaDeCarga.html')

def ReportEvent(request, pk):
     usuario = EmpresaPersona.objects.get(pk=pk)
     contexto = {'usuario': usuario}     
     return render(request, 'view/VistasPCU/ReportEvent.html', contexto)


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



from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.conf import settings


def send_report_email(request, pk):
    print("Entró en send_report_email")

    try:
                # Obtener el objeto del usuario_reportado usando el ID
        # EmpresaPersona = get_user_model()
        # usuario_reportado = EmpresaPersona.objects.get(idregistro=usuario_reportado_id)
        usuario = EmpresaPersona.objects.get(idregistro=pk)

        infraccion1 = request.POST.get('infraccion1')
        infraccion2 = request.POST.get('infraccion2')
        infraccion3 = request.POST.get('infraccion3')
        infraccion4 = request.POST.get('infraccion4')
        infraccion5 = request.POST.get('infraccion5')

        context = {
            'usuario': usuario,
            'infraccion1': infraccion1,
            'infraccion2': infraccion2,
            'infraccion3': infraccion3,
            'infraccion4': infraccion4,
            'infraccion5': infraccion5
            }
        template = get_template('correo_reporte.html')
        content = template.render(context)

        email = EmailMultiAlternatives(
                    'Reporte de usuario',
                    'Probando app parche',
                    settings.EMAIL_HOST_USER,
                    ['contactoparchecorp@gmail.com']
                )

        email.attach_alternative(content, 'text/html')
        email.send()

        print(f"Correo enviado:")
        return HttpResponse("Correo de reporte enviado correctamente")
    except EmpresaPersona.DoesNotExist:
                messages.error(request, 'Usuario no encontrado.')
    except Exception as e:
                print(f"Error al enviar correo de reporte: {e}")
                messages.error(request, 'Error al enviar correo de reporte.')

    return render(request, 'view/VistasPCU/perfil.html')

    

def addLikes(request, pk):
    post = EmpresaPersona.objects.get(pk=pk)

    is_dislikes = False

    for dislikes in post.dislikes.all():
        if dislikes == request.user:
            is_dislikes = True
            break

    if is_dislikes:
        post.dislikes.remove(request.user)

    is_likes = False
    for likes in post.likes.all():
        if likes == request.user:
            is_likes = True
            break

    if not is_likes:
        post.likes.add(request.user)
    else:
        post.likes.remove(request.user)

    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

def adddislike(request, pk):
    post = EmpresaPersona.objects.get(pk=pk)

    is_likes = False
    for likes in post.likes.all():
        if likes == request.user:
            is_likes = True
            break

    if is_likes:
        post.likes.remove(request.user)

    is_dislikes = False
    for dislikes in post.dislikes.all():
        if dislikes == request.user:
            is_dislikes = True
            break

    if not is_dislikes:
        post.dislikes.add(request.user)
    else:
        post.dislikes.remove(request.user)

    next = request.POST.get('next', '')
    return HttpResponseRedirect(next)

def interfazUser(request, empresa_idempresa ):
  form = EmpresaPersona.objects.get(usuario=empresa_idempresa)
  comment = comentarioUSer.objects.filter(receptor=form).order_by('created_on')

  if request.method == 'POST':
    comment = comentarioUserform(request.POST)
    if comment.is_valid():
        newcomment = comment.save(commit=False)
        newcomment.author = request.user
        newcomment.receptor =  EmpresaPersona.objects.get(usuario=empresa_idempresa)
        newcomment.save()
        return redirect('interfaz', empresa_idempresa=form)
    else:
        comment.errors
  return render(request,'view/VistasPCU/interfazdelosUsuarios.html', {'form':form, 'commentUser':comment})

# def Comment(request):
def addCommentLikes(request, id):
    commentUser = comentarioUSer.objects.get(id=id)


    is_dislikes = False

    for dislikes in commentUser.dislikes.all():
        if dislikes == request.user:
            is_dislikes = True
            break

    if is_dislikes:
        commentUser.dislikes.remove(request.user)

    is_likes = False
    for likes in commentUser.likes.all():
        if likes == request.user:
            is_likes = True
            break

    if not is_likes:
        commentUser.likes.add(request.user)
    else:
        commentUser.likes.remove(request.user)

    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

def addCommentDislike(request, id):
    commentUser = comentarioUSer.objects.get(id=id)


    is_likes = False
    for likes in commentUser.likes.all():
        if likes == request.user:
            is_likes = True
            break

    if is_likes:
        commentUser.likes.remove(request.user)

    is_dislikes = False
    for dislikes in commentUser.dislikes.all():
        if dislikes == request.user:
            is_dislikes = True
            break

    if not is_dislikes:
        commentUser.dislikes.add(request.user)
    else:
        commentUser.dislikes.remove(request.user)

    next = request.POST.get('next', '')
    return HttpResponseRedirect(next)

def deleteComment(request, id):
    form = comentarioUSer.objects.get(id=id)
    form.delete()
    print(f"este es el usuario {form.receptor}")
    return redirect('interfaz', empresa_idempresa = form.receptor)

def deleteCommentUser(request, id):
    form = comentarioUSer.objects.get(id=id)
    form.delete()
    print(f"este es el usuario {form.receptor}")
    return redirect('interfaz')

# def replycomment(request, pk):
#  post = comentarioUSer.objects.get(pk = pk)

#  if request.method == 'POST':
#     form = comentarioUserform(request.POST)

#     if form.is_valid()

def joinEvent(request, pk):
    if request.method == 'POST':
        post = joinEventP(request.POST)
        if post.is_valid():
            newpost = post.save(commit=False)
            newpost.usuario_idusuario = request.user
            newpost.save()
            messages.add_message(request=request, level=messages.SUCCESS, message='registro exitoso')
            return redirect('mostrarEventos')
        else:
            print(post.errors)
            messages.add_message(request=request, level=messages.ERROR, message='No puedes unirte de Nuevo')


    return redirect('mostrarEventos')
    


        
     

        
