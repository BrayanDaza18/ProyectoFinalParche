# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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


class Persona(models.Model):
    idpersona = models.AutoField(db_column='idPersona', primary_key=True)  # Field name made lowercase.
    documento = models.CharField(max_length=45)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=45)
    correo = models.CharField(max_length=45)
    telefono = models.IntegerField()
    empresa_idempresa = models.ForeignKey(EmpresaPersona, models.DO_NOTHING, db_column='empresa_idEmpresa')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'persona'
        unique_together = (('idpersona', 'empresa_idempresa'),)


class Puntosdeportivos(models.Model):
    nombre = models.CharField(max_length=50)
    id = models.IntegerField(primary_key=True)
    logo = models.CharField(max_length=80)
    direccion = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'puntosdeportivos'


class Realizacion(models.Model):
    actividad_idactividad = models.OneToOneField(Actividad, models.DO_NOTHING, db_column='actividad_idActividad', primary_key=True)  # Field name made lowercase.
    usuario_idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_idUsuario')  # Field name made lowercase.
    comentarios = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'realizacion'
        unique_together = (('actividad_idactividad', 'usuario_idusuario'),)


class Usuario(models.Model):
    idusuario = models.AutoField(db_column='idUsuario', primary_key=True)  # Field name made lowercase.
    usuario = models.CharField(max_length=40)
    contrasena = models.CharField(max_length=20)
    correo = models.CharField(max_length=45)
    fotoperfil = models.CharField(db_column='fotoPerfil', max_length=80)  # Field name made lowercase.
    resena = models.CharField(max_length=40)
    telefono = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'usuario'
