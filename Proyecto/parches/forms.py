from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (Actividad, Documento, EmpresaPersona, Persona,
                     comentarioUSer)


class FormUser(forms.ModelForm):
    password1 = forms.CharField(label='password', widget= forms.PasswordInput(
        attrs={
            'class': 'form-control, justify-content-center',
            'placeholder': 'ingrese la contraseña',
            'id': 'password',
            'required': 'required',
             'type': 'password'
        }
    ))
    password2 = forms.CharField(label='contreseña de validacion', widget= forms.PasswordInput(
        attrs= {
             'class': 'form-control,justify-content-center',
            'placeholder': 'verifique la contraseña',
            'id': 'password2',
            'required': 'required',
             'type': 'password'
        }
    ))
    class Meta:
        model = EmpresaPersona
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
        # 'nombreempresa': forms.NumberInput(
        #     attrs= {
        #      'class': 'form-control,justify-content-center',
        #     'placeholder': 'nombreempresa',
        #     'id': 'nombreempresa',
       
        # })
        }
    def clean_password2(self):

     password1 = self.cleaned_data.get('password1')
     password2 = self.cleaned_data.get('password2')

     if password1 != password2:
        raise forms.ValidationError('las contraseñas no coinciden')
     return password2

    def save(self, commit = True):
        user = super().save(commit= False)
        user.set_password(self.cleaned_data['password1'])    
        if commit:
          user.save()
        return user
        
    

class UserRegister(forms.ModelForm):
    class Meta:
    
     model = Persona
     fields = ['documento','nombre', 'apellido']
     widgets = {
     'documento': forms.NumberInput( 
         attrs= {
            'class': 'form-control,justify-content-center',
            'placeholder': 'documento',
            'id': 'documento',
            'required': 'required'
      }),
     'nombre': forms.TextInput(
        attrs={
             'class': 'form-control,justify-content-center',
            'placeholder': 'nombre',
            'id': 'nombre',
            'required': 'required'
        }),
      'apellido': forms.TextInput(
        attrs={
             'class': 'form-control,justify-content-center',
            'placeholder': 'apellido',
            'id': 'apellido',
            'required': 'required'
     })
     }
    def save(self, commit = True):
        user = super().save(commit= False)
    
        if commit:
          user.save()
        return user
        

class USERFORM(UserCreationForm):
    class Meta:
     
     model = User
     fields = "__all__"

class FormUserCompany(forms.ModelForm):
    password1 = forms.CharField(label='password', widget= forms.PasswordInput(
        attrs={
            'class': 'form-control, justify-content-center',
            'placeholder': 'ingrese la contraseña',
            'id': 'password',
            'required': 'required'
        }
    ))
    password2 = forms.CharField(label='contreseña de validacion', widget= forms.PasswordInput(
        attrs= {
             'class': 'form-control,justify-content-center',
            'placeholder': 'verifique la contraseña',
            'id': 'password2',
            'required': 'required'
        }
    ))
    class Meta:
        model = EmpresaPersona
        fields = ('usuario', 'correo', 'telefono', 'nombreempresa','direccion')
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
        }), 
        'nombreempresa': forms.TextInput(
                 attrs= {
            'class': 'form-control, justify-content-center',
            'placeholder': 'nombreEmpresa',
            'id': 'nombreempresa',
            'required': 'required'
        }),
        'direccion': forms.TextInput(
            attrs= {
             'class': 'form-control,justify-content-center',
            'placeholder': 'direccion',
            'id': 'direccion',
       
        })
        }
    def clean_password2(self):

     password1 = self.cleaned_data.get('password1')
     password2 = self.cleaned_data.get('password2')

     if password1 != password2:
        raise forms.ValidationError('las contraseñas no coinciden')
     return password2

    def save(self, commit = True):
        user = super().save(commit= False)
        user.set_password(self.cleaned_data['password1'])    
        if commit:
          user.save()
        return user

class Document(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['documentocol']
        widgets = {
            'documentocol': forms.FileInput(attrs={
                'class': 'justify-content-center',
                'placeholder': 'documento',
                'id': 'input-file',
                'style': 'display: none',
                'required': 'required'
            })
        }
    def save(self, commit = True):
        user = super().save(commit= False)  
        if commit:
          user.save()
        return user


class CreateEventos(forms.ModelForm):

    class Meta:
        model = Actividad
        fields = ['nombreactividad', 'tipoactividad', 'lugar', 'fechainicio','fechafin','hora','imagen', 'contacto','descripcion']
        widgets = {
            'nombreactividad': forms.TextInput(
            attrs= {
            'class': 'form-control,justify-content-center',
            'placeholder': 'nombreactividad',
            'id': 'nombreactividad',
            'required': 'required'
        }),
           
        'lugar': forms.TextInput(
            attrs= {
             'class': 'form-control,justify-content-center',
            'placeholder': 'lugar',
            'id': 'lugar',
            'required': 'required'
        }), 
        'fechainicio': forms.DateInput(
                 attrs= {
            'class': 'form-control, justify-content-center',
            'placeholder': 'fechainicio',
            'id': 'fechainicio',
            'required': 'required'
        }),
        'fechafin': forms.DateInput(
            attrs= {
             'class': 'form-control,justify-content-center',
            'placeholder': 'fechafin',
            'id': 'fechafin',
       
        }),
         'hora': forms.TimeInput(
            attrs= {
             'class': 'form-control,justify-content-center',
            'placeholder': 'hora',
            'id': 'hora',
       
        }),
          'imagen': forms.FileInput(
            attrs= {
             'class': 'form-control,justify-content-center',
            'placeholder': 'imagen',
            'id': 'imagen',
       
        }),
          'contacto': forms.NumberInput(
            attrs= {
             'class': 'form-control,justify-content-center',
            'placeholder': 'contacto',
            'id': 'contacto',
       
        }),
        'descripcion': forms.Textarea(
            attrs= {
             'class': 'form-control,justify-content-center',
            'placeholder': 'descripcion',
            'id': 'descripcion',
       
        }),
        }
    
    def save(self, commit = True):
        user = super().save(commit= False)  
        if commit:
          user.save()
        return user

class FormUserUpdate(forms.ModelForm):

    class Meta:
        model = EmpresaPersona
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
        }),
        #   'password': forms.PasswordInput(
        #     attrs= {
        #      'class': 'justify-content-center',
        #     'placeholder': 'password',
        #     'id': 'password',
        #     'required': 'required',
        #     'type': 'password'
        # })
        # 'nombreempresa': forms.NumberInput(
        #     attrs= {
        #      'class': 'form-control,justify-content-center',
        #     'placeholder': 'nombreempresa',
        #     'id': 'nombreempresa',
       
        # })
        }
class FormCompanyUpdate(forms.ModelForm):

     class Meta:
        model = EmpresaPersona
        fields = ('usuario', 'correo', 'telefono', 'nombreempresa','direccion')
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
            'id': 'telefono',
            'required': 'required'
        }),
        }

class comentarioUserform(forms.ModelForm):
     class Meta:
        model = comentarioUSer
        fields = ['comment']
        widgets = {
            'comment': forms.TextInput(
                 attrs= {
            'class': 'form-control,justify-content-center',
            'placeholder': 'comment',
            'id': 'comment',
            'required': 'required'
        }),
        }
