from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.urls import include, path

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
    path('updateUserCompany/<int:idregistro>/<str:tipousuario>', views.UpdateUserCompany, name='UpdateUserCompany')
    
]