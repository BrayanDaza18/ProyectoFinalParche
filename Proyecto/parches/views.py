from datetime import datetime
from smtplib import SMTPException
from folium import Marker
import folium
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from folium import Marker

from .forms import (CreateEventos, Document, FormCompanyUpdate, FormUser,
                    FormUserCompany, FormUserUpdate, ResenaEventoF,
                    UserRegister, comentarioUserform, joinEventP)
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

    if request.method == 'POST':
        form = FormUser(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            if EmpresaPersona.objects.filter(correo=correo).exists():
                form.add_error('correo', 'El correo ya está asociado a otra cuenta.')
                return render(request, 'registration/register.html', {'form': form})

            usuario = form.cleaned_data['usuario']
            if EmpresaPersona.objects.filter(usuario=usuario).exists():
                form.add_error('usuario', 'El nombre de usuario ya está en uso.')
                return render(request, 'registration/register.html', {'form': form})

            data = form.save(commit=False)
            data.tipousuario = 'U'
            data.save()

            now = datetime.now()
            fecha_hora_actual = now.strftime("%Y-%m-%d %H:%M:%S")
            send_email(correo, usuario, fecha_hora_actual)
           
            return redirect('login')

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
@login_required
def CreateEvent(request):
    activity = CreateEventos()
    if request.method == 'POST':
        activity = CreateEventos(request.POST, request.FILES)
        if activity.is_valid():
            usuario = activity.save(commit=False)
            usuario.empresa_idempresa = request.user
            usuario.estado = 'activo'
            usuario.save()
            return redirect('vistaPrincipal')
        else:
            print("Errores en el formulario CreateEventos:", activity.errors)
            messages.add_message(request=request, level=messages.ERROR, message='datos incompletos')

        
    
    return render(request, 'view/VistasPCU/crearEvento.html', {'activity': activity})



def RegisterCompany(request):
    document_form = Document()  
    form = FormUserCompany()

    if request.method == 'POST':
        form = FormUserCompany(request.POST)
        document_form = Document(request.POST, request.FILES) 

        if form.is_valid() and document_form.is_valid():
            correo = form.cleaned_data['correo']
            if EmpresaPersona.objects.filter(correo=correo).exists():
                form.add_error('correo', 'El correo ya está asociado a otra cuenta.')
                return render(request, 'registration/registroEmpresa.html', {'document': document_form, 'form': form})

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

            return redirect('login')
        else:
            print("Errores en el formulario FormUserCompany:", form.errors)
            print("Errores en el formulario Document:", document_form.errors)
            return render(request, 'registration/registroEmpresa.html', {'document': document_form, 'form': form})

    return render(request, 'registration/registroEmpresa.html', {'document': document_form, 'form': form})



@login_required
def MostrarEvento(request):
    messageEnd()
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

@login_required
def Profile(request):
    
    usuario = request.user
    if usuario:
        form = Actividad.objects.filter(empresa_idempresa=usuario)
        send = Realizacion.objects.filter(usuario_idusuario=usuario)
        comment = comentarioUSer.objects.filter(author = usuario).order_by('created_on')
        actividad = EmpresaPersona.objects.get(usuario = usuario)

    if request.method == 'POST':
       comment = comentarioUserform(request.POST)

       if comment.is_valid():
            commentUser = comment.save(commit=False)
            commentUser.author = request.user
            commentUser.receptor = request.user
            commentUser.save()
            return redirect('profile')
      
    return render(request, 'view/VistasPCU/perfil.html', {'data': form, 'actividad': actividad, 'comment': comment,'send':send})


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
    data = Actividad.objects.get(pk=idactividad)
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
        motivo = request.POST.get('motivo')

        infraccion1 = request.POST.get('infraccion1')
        infraccion2 = request.POST.get('infraccion2')
        infraccion3 = request.POST.get('infraccion3')
        infraccion4 = request.POST.get('infraccion4')
        infraccion5 = request.POST.get('infraccion5')

        context = {
            'usuario': usuario,
            'motivo': motivo,
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


from django.shortcuts import get_object_or_404


def joinEvent(request, pk):
    
    if request.method == 'POST':
        post = joinEventP(request.POST)
        if post.is_valid():
            if Realizacion.objects.filter(actividad_idactividad=pk, usuario_idusuario=request.user).exists():
                messages.error(request, 'Ya estás inscrito en esta actividad.')
                return redirect('mostrarEventos')
            newpost = post.save(commit=False)
            newpost.usuario_idusuario = request.user
            newpost.save()
            
            usuario_correo = request.user.correo
            usuario_nombre = request.user.usuario
            evento_nombre = newpost.actividad_idactividad.nombreactividad
            fecha_inicio_evento = newpost.actividad_idactividad.fechainicio
            hora_inicio_evento = newpost.actividad_idactividad.hora

            send_event_notification(usuario_correo, usuario_nombre, evento_nombre, fecha_inicio_evento, hora_inicio_evento)

            messages.add_message(request=request, level=messages.SUCCESS, message='registro exitoso')
            return redirect('mostrarEventos')
        else:
            print(post.errors)
            messages.add_message(request=request, level=messages.ERROR, message='No puedes unirte de nuevo')

    return redirect('mostrarEventos')



def eventoRegistration(request):
    send = Realizacion.objects.filter(usuario_idusuario=request.user) 
    form = Actividad.objects.filter(idactividad__in=send.values('actividad_idactividad'))
    print(f"elemento{form}")
    return render(request, 'view/VistasPCU/eventoEgistration.html', {'data':form})
    

def deleteRegistration(request,idactividad):
    post = Realizacion.objects.get(actividad_idactividad= idactividad,usuario_idusuario= request.user)
    post.delete()
    return redirect('inscripcion')



def send_event_notification(usuario_correo, usuario_nombre, evento_nombre, fecha_inicio_evento, hora_inicio_evento):
    try:
        context = {
            'usuario_correo': usuario_correo,
            'usuario_nombre': usuario_nombre,
            'evento_nombre': evento_nombre,
            'fecha_inicio_evento': fecha_inicio_evento,
            'hora_inicio_evento': hora_inicio_evento,
        }
        template = get_template('evento_notificacion.html')
        content = template.render(context)
        
        email = EmailMultiAlternatives(
            'Unión a evento',
            '¡Te has unido a un nuevo evento!',
            settings.EMAIL_HOST_USER,
            [usuario_correo]
        )

        email.attach_alternative(content, 'text/html')
        email.send()

    except (ValidationError, SMTPException) as e:
        print(f"Error al enviar correo de notificación de evento: {e}")
        
        
def ReportEvent(request, pk):
     usuario = EmpresaPersona.objects.get(pk=pk)
     contexto = {'usuario': usuario}     
     return render(request, 'view/VistasPCU/ReportEvent.html', contexto)
     
     
def send_report_email(request, pk):
    print("Entró en send_report_email")

    try:
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
        print("no funciono")
        
    return render(request, 'view/VistasPCU/perfil.html')

        
def eventParticipante(request, pk):
    activity = Actividad.objects.get(pk=pk)
    send = Realizacion.objects.filter(actividad_idactividad=pk).values('usuario_idusuario').distinct()
    form = EmpresaPersona.objects.filter(idregistro__in=send)
    
   
    return render(request, 'view/VistasPCU/viewEventcompetitor.html',{'form':form, 'activity': activity})

def anularinscripcion(request, idregistro, pk):

 form = Realizacion.objects.get(actividad_idactividad= pk, usuario_idusuario= idregistro)
 form.delete()
 return redirect('participantes', pk=pk)


def messageEnd():
    userFinally = Actividad.objects.all()
    for element in userFinally:
        if element.fechafin  < str(datetime.now().date()):
           element.estado = 'finalizado'
           element.save()
           realizar = Realizacion.objects.filter(actividad_idactividad = element.idactividad)
           
           for realizarc in realizar:
            if realizarc.usuario_idusuario and element.estado == 'finalizado':
                usuario = realizarc.usuario_idusuario
                evento = realizarc.actividad_idactividad
                print(usuario)
                try:
                   context = {'correo': usuario.correo, 'usuario': usuario.usuario, 'current_datetime': element.fechafin, 'idEvento': evento.pk}
                   template = get_template('correo_finalizacion.html')
                   content = template.render(context)
                   print( usuario.correo)
                   print(usuario)

                   email = EmailMultiAlternatives(
                   'El evento a finalizado',  # Título
                   'Probando app parche',  # Descripción
                   settings.EMAIL_HOST_USER,  # Quién envía el correo
                   [usuario.correo])

                   email.attach_alternative(content, 'text/html')
                   email.send()

                except (ValidationError, SMTPException) as e:
                  print(f"Error al enviar correo: {e}")


def calificacionFinal(request, idEvento):
    
    evento = Realizacion.objects.get(actividad_idactividad= idEvento,usuario_idusuario= request.user )
    resena = ResenaEventoF()
    
    if request.method == 'POST':
        resena = ResenaEventoF(request.POST or None, instance=evento)
        if resena.is_valid() :
            
            resena.save()
    
    return render(request, 'view/VistasPCU/ResenaFinalCalificacion.html', {'data':resena})





#Api de actividades sin autenticacion
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import ActividadSerializer, EmpresaPersonaSerializer


class ActividadListAPIView(generics.ListAPIView):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
    permission_classes = [AllowAny] 

class ActividadDetailAPIView(generics.RetrieveAPIView):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
    permission_classes = [AllowAny]  
    
class EmpresaPersonaListAPIView(generics.ListAPIView):
    queryset = EmpresaPersona.objects.all()
    serializer_class = EmpresaPersonaSerializer
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación

class EmpresaPersonaDetailAPIView(generics.RetrieveAPIView):
    queryset = EmpresaPersona.objects.all()
    serializer_class = EmpresaPersonaSerializer
    permission_classes = [AllowAny] 
    
#con autenticación 
# class ActividadListAPIView(generics.ListAPIView):
#     queryset = Actividad.objects.all()
#     serializer_class = ActividadSerializer
#     permission_classes = [IsAuthenticated]

# class ActividadDetailAPIView(generics.RetrieveAPIView):
#     queryset = Actividad.objects.all()
#     serializer_class = ActividadSerializer
#     permission_classes = [IsAuthenticated]
