from django.shortcuts import render

# Create your views here.

def HomepageProject(request):
     return render(request, 'view/VistasPCU/vistaPrincipal.html' )

def registerUser(request):
     return render(request, 'view/VistasPCU/registro.html')

def login(request):
     return render(request, 'view/VistasPCU/login.html')

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