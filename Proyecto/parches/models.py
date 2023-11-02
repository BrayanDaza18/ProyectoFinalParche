# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class Actividad(models.Model):
    idactividad = models.IntegerField(db_column='idActividad', primary_key=True)  # Field name made lowercase.
    nombreactividad = models.CharField(db_column='nombreActividad', max_length=30)  # Field name made lowercase.
    tipoactividad = models.CharField(db_column='tipoActividad', max_length=10)  # Field name made lowercase.
    lugar = models.CharField(max_length=40)
    ubicacion = models.CharField(max_length=80)
    fechainicio = models.DateField(db_column='fechaInicio')  # Field name made lowercase.
    fechafin = models.DateField(db_column='fechaFin')  # Field name made lowercase.
    hora = models.TimeField()
    imagen = models.CharField(max_length=80)
    contacto = models.CharField(max_length=30)
    puntosdeportivos = models.ForeignKey('Puntosdeportivos', models.DO_NOTHING)
    empresa_idempresa = models.ForeignKey('EmpresaPersona', models.DO_NOTHING, db_column='empresa_idEmpresa')  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'actividad'
        unique_together = (('idactividad', 'puntosdeportivos', 'empresa_idempresa'),)


class Documento(models.Model):
    iddocumento = models.IntegerField(db_column='idDocumento', primary_key=True)  # Field name made lowercase.
    documentocol = models.CharField(db_column='Documentocol', max_length=45, blank=True, null=True)  # Field name made lowercase.
    empresa_idempresa = models.ForeignKey('EmpresaPersona', models.DO_NOTHING, db_column='empresa_idEmpresa')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'documento'
        unique_together = (('iddocumento', 'empresa_idempresa'),)


class EmpresaPersona(models.Model):
    idregistro = models.AutoField(db_column='idRegistro', primary_key=True)  # Field name made lowercase.
    nit = models.CharField(max_length=45, blank=True, null=True)
    nombreempresa = models.CharField(db_column='nombreEmpresa', unique=True, max_length=40)  # Field name made lowercase.
    direccion = models.CharField(max_length=40)
    correo = models.CharField(max_length=40)
    contrasena = models.CharField(max_length=45)
    telefono = models.CharField(max_length=40)
    tipousuario = models.CharField(db_column='tipoUsuario', max_length=1)  # Field name made lowercase.

   
    class Meta:
        managed = False
        db_table = 'empresa/persona'


class Persona(models.Model ):
    idpersona = models.AutoField(db_column='idPersona', primary_key=True)
    documento = models.CharField(max_length=45)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=45)
    correo = models.CharField(max_length=45)
    telefono = models.IntegerField()
    
 

    # Puedes agregar métodos personalizados y lógica de autenticación aquí

    class Meta:
        managed = False
        db_table = 'persona'


class Puntosdeportivos(models.Model):
    nombre = models.CharField(max_length=50)
    id = models.IntegerField(primary_key=True)
    logo = models.CharField(max_length=80)
    direccion = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'puntosdeportivos'


class Realizacion(models.Model):
    actividad_idactividad = models.OneToOneField(Actividad, models.DO_NOTHING, db_column='actividad_idActividad', primary_key=True) 
    usuario_idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_idUsuario')  
    comentarios = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'realizacion'
        unique_together = (('actividad_idactividad', 'usuario_idusuario'),)




class UsuarioManager(BaseUserManager):
    def create_user(self, usuario, correo, telefono, password):
        usuario = self.model(usuario=usuario, correo=correo, telefono=telefono)
        usuario.usuario_activo = True
        usuario.set_password(password)  
        usuario.save()
        return usuario

    def create_superuser(self, usuario, password):
        usuario = self.create_user(usuario=usuario, correo="", telefono=0, password=password)
        usuario.usuario_administrador = True
        usuario.save()
        return usuario

        
class Usuario(AbstractBaseUser, PermissionsMixin):
    idusuario = models.AutoField(db_column='idUsuario', primary_key=True)
    usuario = models.CharField(max_length=40, db_column='usuario', unique=True)
    password = models.CharField(max_length=128) 
    correo = models.CharField(max_length=45)
    fotoperfil = models.CharField(db_column='fotoPerfil', max_length=80)
    resena = models.CharField(max_length=40)
    telefono = models.IntegerField(null=True)
    usuario_activo = models.BooleanField(default= True)
    usuario_administrador = models.BooleanField(default= False)
    


    # Configura los campos requeridos al crear un usuario
    REQUIRED_FIELDS = ['correo', 'telefono']  # Agrega aquí los campos adicionales requeridos
    USERNAME_FIELD = 'usuario'
    # PASSWORD_FIELD = 'contrasena'  # No necesitas especificar esto, se utiliza el campo "password" por defecto

    objects = UsuarioManager()

    def __str__(self):
        return self.usuario

    def has_perm(self,perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador

    # class Meta:
    #     managed = False
    #     db_table = 'usuario'