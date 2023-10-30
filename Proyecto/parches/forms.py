from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Usuario


class FormUser(forms.ModelForm):
    password = forms.CharField(label='contrasena', widget= forms.PasswordInput(
        attrs={
            'class': 'form-control, justify-content-center',
            'placeholder': 'ingrese la contraseña',
            'id': 'password1',
            'required': 'required'
        }
    ))
    password2 = forms.CharField(label='contrasena', widget= forms.PasswordInput(
        attrs= {
             'class': 'form-control,justify-content-center',
            'placeholder': 'verifique la contraseña',
            'id': 'password2',
            'required': 'required'
        }
    ))
    class Meta:
        model = Usuario
        fields = ('usuario', 'correo', 'telefono')
        widgets = {
            'usuario': forms.TextInput(
                 attrs= {
             'class': 'form-control,justify-content-center',
            'placeholder': 'usuario',
            'id': 'usuario',
            'required': 'required'
        }),
            'correo': forms.EmailInput( 
                attrs= {
             'class': 'form-control,justify-content-center',
            'placeholder': 'correo',
            'id': 'email',
            'required': 'required'
        }),
        'telefono': forms.NumberInput(
            attrs= {
             'class': 'form-control,justify-content-center',
            'placeholder': 'telefono',
            'id': 'email',
            'required': 'required'
        })
        }
        

class USERFORM(UserCreationForm):
    class Meta:
     
     model = User
     fields = "__all__"

