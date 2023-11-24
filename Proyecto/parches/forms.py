from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from .models import (Actividad, Documento, EmpresaPersona, Persona, Realizacion, comentarioUSer)


def validate_password(value):
    if len(value) < 8:
        raise ValidationError('La contraseña debe tener al menos 8 caracteres.')

    if not any(char.isdigit() for char in value):
        raise ValidationError('La contraseña debe contener al menos un número.')

    special_characters = r"[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
    if not re.search(special_characters, value):
        raise ValidationError('La contraseña debe contener al menos un carácter especial.')


class FormUser(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control, justify-content-center',
                'placeholder': 'Ingrese la contraseña',
                'id': 'password',
                'required': 'required',
                'type': 'password'
            }
        ),
        validators=[validate_password]  # Agrega la validación personalizada
    )

    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control,justify-content-center',
                'placeholder': 'Verifique la contraseña',
                'id': 'password2',
                'required': 'required',
                'type': 'password'
            }
        ),
    )

    class Meta:
        model = EmpresaPersona
        fields = ('usuario', 'correo', 'telefono')
        widgets = {
            'usuario': forms.TextInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Usuario',
                    'id': 'usuario',
                    'required': 'required'
                }),
            'correo': forms.EmailInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Correo',
                    'id': 'email',
                    'required': 'required'
                }),
            'telefono': forms.NumberInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Teléfono',
                    'id': 'telefono',
                    'required': 'required'
                }),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserRegister(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['documento', 'nombre', 'apellido']
        widgets = {
            'documento': forms.NumberInput(
                attrs={
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

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class USERFORM(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"


class FormUserCompany(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control, justify-content-center',
                'placeholder': 'Ingrese la contraseña',
                'id': 'password',
                'required': 'required'
            }
        ),
        validators=[validate_password]  # Agrega la validación personalizada
    )

    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control,justify-content-center',
                'placeholder': 'Verifique la contraseña',
                'id': 'password2',
                'required': 'required'
            }
        ),
    )

    class Meta:
        model = EmpresaPersona
        fields = ('usuario', 'correo', 'telefono', 'nombreempresa', 'direccion')
        widgets = {
            'usuario': forms.TextInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Usuario',
                    'id': 'usuario',
                    'required': 'required'
                }),
            'correo': forms.EmailInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Correo',
                    'id': 'email',
                    'required': 'required'
                }),
            'telefono': forms.NumberInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Teléfono',
                    'id': 'telefono',
                    'required': 'required'
                }),
            'nombreempresa': forms.TextInput(
                attrs={
                    'class': 'form-control, justify-content-center',
                    'placeholder': 'Nombre de la Empresa',
                    'id': 'nombreempresa',
                    'required': 'required'
                }),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Dirección',
                    'id': 'direccion',

                })
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
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

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class CreateEventos(forms.ModelForm):

    class Meta:
        model = Actividad
        fields = ['nombreactividad', 'tipoactividad', 'lugar', 'fechainicio', 'fechafin', 'hora', 'imagen', 'contacto', 'descripcion']
        widgets = {
            'nombreactividad': forms.TextInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Nombre de la Actividad',
                    'id': 'nombreactividad',
                    'required': 'required'
                }),

            'lugar': forms.TextInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Lugar',
                    'id': 'lugar',
                    'required': 'required'
                }),
            'fechainicio': forms.DateInput(
                attrs={
                    'class': 'form-control, justify-content-center',
                    'placeholder': 'Fecha de Inicio',
                    'id': 'fechainicio',
                    'required': 'required'
                }),
            'fechafin': forms.DateInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Fecha de Fin',
                    'id': 'fechafin',

                }),
            'hora': forms.TimeInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Hora',
                    'id': 'hora',

                }),
            'imagen': forms.FileInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Imagen',
                    'id': 'imagen',

                }),
            'contacto': forms.NumberInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Contacto',
                    'id': 'contacto',

                }),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Descripción',
                    'id': 'descripcion',

                }),
        }

    latitud = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitud = forms.FloatField(widget=forms.HiddenInput(), required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.latitud = self.cleaned_data.get('latitud', 0)
        user.longitud = self.cleaned_data.get('longitud', 0)

        if commit:
            user.save()
        return user


class FormUserUpdate(forms.ModelForm):

    class Meta:
        model = EmpresaPersona
        fields = ('usuario', 'correo', 'telefono')
        widgets = {
            'usuario': forms.TextInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Usuario',
                    'id': 'usuario',
                    'required': 'required'
                }),
            'correo': forms.EmailInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Correo',
                    'id': 'email',
                    'required': 'required'
                }),
            'telefono': forms.NumberInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Teléfono',
                    'id': 'email',
                    'required': 'required'
                }),
        }


class FormCompanyUpdate(forms.ModelForm):

    class Meta:
        model = EmpresaPersona
        fields = ('usuario', 'correo', 'telefono', 'nombreempresa', 'direccion')
        widgets = {
            'usuario': forms.TextInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Usuario',
                    'id': 'usuario',
                    'required': 'required'
                }),
            'correo': forms.EmailInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Correo',
                    'id': 'email',
                    'required': 'required'
                }),
            'telefono': forms.NumberInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Teléfono',
                    'id': 'telefono',
                    'required': 'required'
                }),
            'nombreempresa': forms.TextInput(
                attrs={
                    'class': 'form-control, justify-content-center',
                    'placeholder': 'Nombre de la Empresa',
                    'id': 'nombreempresa',
                    'required': 'required'
                }),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Dirección',
                    'id': 'direccion',

                })
        }


class comentarioUserform(forms.ModelForm):
    class Meta:
        model = comentarioUSer
        fields = ['comment']
        widgets = {
            'comment': forms.TextInput(
                attrs={
                    'class': 'form-control,justify-content-center',
                    'placeholder': 'Comentario',
                    'id': 'comment',
                    'required': 'required'
                }),
        }


class joinEventP(forms.ModelForm):
    class Meta:
        model = Realizacion
        fields = ['actividad_idactividad']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
