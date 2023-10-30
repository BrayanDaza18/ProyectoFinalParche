from django.urls import include, path

from . import views

urlpatterns = [
    
    path('', views.HomepageProject, name='vistaPrincipal'),
    path('Register/User', views.registerUser, name='register'),
    path('login', views.login, name='login'),
    path('CreateEvent', views.CreateEvent, name='CreateEvent'),
    path('Register/Company', views.RegisterCompany, name='RegisterCompany'),
    path('profile', views.Profile, name='profile'),
    path('coverImage', views.CoverImage, name='CoverImagen'),
    path('Report', views.ReportEvent, name='Report'),
     
    
]