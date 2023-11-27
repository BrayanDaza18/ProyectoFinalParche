from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmpresaPersona',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('idregistro', models.AutoField(db_column='idRegistro', primary_key=True, serialize=False)),
                ('nit', models.CharField(blank=True, max_length=45, null=True)),
                ('usuario', models.CharField(db_column='usuario', max_length=40, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('nombreempresa', models.CharField(db_column='nombreEmpresa', max_length=40, null=True, unique=True)),
                ('direccion', models.CharField(max_length=40)),
                ('correo', models.CharField(max_length=45)),
                ('telefono', models.CharField(max_length=40)),
                ('tipousuario', models.CharField(choices=[('E', 'E'), ('U', 'U')], db_column='tipoUsuario', max_length=1)),
                ('fotoperfil', models.CharField(db_column='fotoPerfil', max_length=80)),
                ('resena', models.CharField(max_length=40)),
                ('usuario_activo', models.BooleanField(default=True)),
                ('usuario_administrador', models.BooleanField(default=False)),
                ('estado', models.CharField(choices=[('A', 'A'), ('I', 'I')], default='I', max_length=1)),
                ('is_active', models.BooleanField(default=True)),
                ('dislikes', models.ManyToManyField(blank=True, related_name='_parches_empresapersona_dislikes_+', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('likes', models.ManyToManyField(blank=True, related_name='_parches_empresapersona_likes_+', to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'empresa/usuario',
            },
        ),
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('idactividad', models.AutoField(db_column='idActividad', primary_key=True, serialize=False)),
                ('nombreactividad', models.CharField(db_column='nombreActividad', max_length=30)),
                ('tipoactividad', models.CharField(choices=[('FUTBOL', 'Futbol'), ('Baloncesto', 'Baloncesto'), ('Juego de mesa', 'Juegos De Mesa'), ('Voleibol', 'Voleibol'), ('Pasar el rato', 'Pasar el rato'), ('natacion', 'Natacion'), ('patinaje', 'Patinaje'), ('tenis', 'Tenis'), ('ciclismo', 'Cilcismo')], db_column='tipoActividad', max_length=15)),
                ('lugar', models.CharField(max_length=40)),
                ('ubicacion', models.CharField(max_length=80)),
                ('fechainicio', models.CharField(db_column='fechaInicio', max_length=40)),
                ('fechafin', models.CharField(db_column='fechaFin', max_length=40)),
                ('descripcion', models.TextField(blank=True, db_column='descripcion', max_length=75, null=True)),
                ('hora', models.CharField(max_length=40)),
                ('imagen', models.ImageField(max_length=80, upload_to='actividad/')),
                ('contacto', models.CharField(max_length=30)),
                ('latitud', models.FloatField(blank=True, null=True)),
                ('longitud', models.FloatField(blank=True, null=True)),
                ('empresa_idempresa', models.ForeignKey(db_column='empresa_idEmpresa', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'actividad',
            },
        ),
        migrations.CreateModel(
            name='Puntosdeportivos',
            fields=[
                ('nombre', models.CharField(max_length=50)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('logo', models.CharField(max_length=80)),
                ('direccion', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'puntosdeportivos',
            },
        ),
        migrations.CreateModel(
            name='Realizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentarios', models.CharField(max_length=45)),
                ('actividad_idactividad', models.ForeignKey(db_column='actividad_idActividad', on_delete=django.db.models.deletion.CASCADE, to='parches.actividad')),
                ('usuario_idusuario', models.ForeignKey(db_column='usuario_idEmpresaPersona', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'realizacion',
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('idpersona', models.AutoField(db_column='idPersona', primary_key=True, serialize=False)),
                ('documento', models.CharField(max_length=45)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=45)),
                ('correo', models.CharField(max_length=45)),
                ('telefono', models.CharField(max_length=40)),
                ('empresa_idEmpresa', models.ForeignKey(db_column='empresa_idEmpresa', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'persona',
            },
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('iddocumento', models.AutoField(db_column='idDocumento', primary_key=True, serialize=False)),
                ('documentocol', models.FileField(db_column='Documentocol', upload_to='documentos/')),
                ('empresa_idempresa', models.ForeignKey(db_column='empresa_idEmpresa', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'documento',
            },
        ),
        migrations.CreateModel(
            name='comentarioUSer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(db_column='comentario')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_author', to=settings.AUTH_USER_MODEL)),
                ('dislikes', models.ManyToManyField(blank=True, related_name='comment_dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL)),
                ('receptor', models.ForeignKey(db_column='usuario', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='actividad',
            name='puntosdeportivos',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='parches.puntosdeportivos'),
        ),
        migrations.AlterUniqueTogether(
            name='actividad',
            unique_together={('idactividad', 'puntosdeportivos', 'empresa_idempresa')},
        ),
    ]
