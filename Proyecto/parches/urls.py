from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.urls import include, path
from .views import ActividadListAPIView, ActividadDetailAPIView, EmpresaPersonaListAPIView, EmpresaPersonaDetailAPIView
from . import views

urlpatterns = [
    
    path('', views.HomepageProject, name='vistaPrincipal', ),
    path('Register/User', views.registerUser, name='register'),
    path('login', views.login, name='login'),
    path('CreateEvent', views.CreateEvent, name='CreateEvent'),
    path('Register/Company', views.RegisterCompany, name='RegisterCompany'),
    path('profile', views.Profile, name='profile'),
    path('coverImage', views.CoverImage, name='CoverImagen'),
    path('Report', views.ReportEvent, name='Report'),
    path('select/user', views.SelectUser, name='selectUser'),
    path('eventCreate',views.eventForUser, name='eventUser' ),
    path('eliminar/<int:idactividad>', views.viewEventoELI, name='eliminar'),
    path('Update/<int:idactividad>', views.UpdateEvent, name='update'),
    path('updateUser/<int:idregistro>/<str:tipousuario>', views.UpdateUser, name='UpdateUser'),
    path('updateUserCompany/<int:idregistro>/<str:tipousuario>', views.UpdateUserCompany, name='UpdateUserCompany'),
    path('eventos', views.MostrarEvento, name='mostrarEventos'),
    path('eliminar/<int:idactividad>', views.viewEventoELI, name='eliminar'),
    
    path('detalles/<int:idactividad>/', views.DetallesEvento, name='detalles_evento'),
    path('profile/dislikes/<int:pk>', views.adddislike, name='dislike'),
    path('profile/likes/<int:pk>', views.addLikes, name='likes'),
    path('interfaz/<str:empresa_idempresa>/User', views.interfazUser, name='interfaz'),
    path('profile/dislikes/<int:id>/comment', views.addCommentDislike, name='dislikecomment'),
    path('profile/likes/<int:id>/comment', views.addCommentLikes, name='likescomment'),
    path('profile/delete/<int:id>/comment', views.deleteComment, name='deleteComment'),
    path('profile/delete/<int:id>/comment', views.deleteCommentUser, name='deleteCommentUser'),
    path('join/event/<int:pk>', views.joinEvent, name='joinEvent'),
    path('evento/inscripcion/', views.eventoRegistration , name='inscripcion'),
    path('evento/inscripcion/anular/<int:idactividad>', views.deleteRegistration , name='inscripcionDeletes'),
    path('reportar_usuario/<int:pk>/', views.send_report_email, name='report'),
    path('Report/<int:pk>/', views.ReportEvent, name='Report'),
    path('puntoDeportivo', views.agregarPd, name='puntoDeportivo'),
    
    
    path('api/actividades/', ActividadListAPIView.as_view(), name='actividad-list'),
    path('api/actividades/<int:pk>/', ActividadDetailAPIView.as_view(), name='actividad-detail'),
    path('api/usuarios/', EmpresaPersonaListAPIView.as_view(), name='usuario-list'),
    path('api/usuarios/<int:pk>/', EmpresaPersonaDetailAPIView.as_view(), name='usuario-detail'),
]