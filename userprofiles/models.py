from __future__ import unicode_literals

# Create your models here.
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from .managers import UserManager

#Django Third packages

# Reason for use UserManager
# http://stackoverflow.com/questions/14723099/attributeerror-manager-object-has-no-attribute-get-by-natural-key-error-in

# Reasons for Manager Methods
# https://docs.djangoproject.com/en/1.9/topics/db/managers/
# https://docs.djangoproject.com/en/dev/ref/contrib/auth/#manager-methods

# Create your models here.
# Reason for use UserManager
# http://stackoverflow.com/questions/14723099/attributeerror-manager-object-has-no-attribute-get-by-natural-key-error-in

# Reasons for Manager Methods
# https://docs.djangoproject.com/en/1.9/topics/db/managers/
# https://docs.djangoproject.com/en/dev/ref/contrib/auth/#manager-methods

# Extending Django's default User
# https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#extending-django-s-default-user
# We inherit from AbstractUser class to add some fields/attibutes to our user model
# https://github.com/django/django/blob/master/django/contrib/auth/models.py#L297
# Differentes between AbstractUser and AbstractBaseUser
# http://stackoverflow.com/questions/21514354/difference-between-abstractuser-and-abstractbaseuser-in-django

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    # Using PermissionsMixin
    # http://stackoverflow.com/questions/31370333/custom-django-user-object-has-no-attribute-has-module-perms

    # http://stackoverflow.com/questions/25239164/issue-with-createsuperuser-when-implementing-custom-user-model
    # required ...
    username = models.CharField(
        max_length=25,
        #unique=True,
        verbose_name='Nombre de usuario'

        # db_index=True)
    )

    first_name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name='Nombres'
    )
    last_name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name='Apellidos'
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de nacimiento',
        help_text="Por favor use el siguiente formato: <em>DD/MM/YYYY</em>.",
    )

    address = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Dirección de residencia'
    )

    phone = models.CharField(
        verbose_name=u'Número de contacto',
        max_length=25,
        blank=True
    )

    occupation = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Ocupación'

    )

    email = models.EmailField(
        max_length=50,
        unique=True
    )

    photo = models.ImageField(
        upload_to='avatars',
        blank=True,
        verbose_name='Imágen de perfil',
        null=True
    )

    age = models.PositiveSmallIntegerField(
        blank=True,
        verbose_name='Edad',
        null=True
    )

    GENDER_CHOICES = (
        ('Femenino', "Femenino"),
        ('Masculino', "Masculino"),
    )
    sex = models.CharField(
        choices=GENDER_CHOICES,
        max_length=12,
        default=False,
        # blank=False,
        verbose_name='Sexo',
    )

    COLOMBIA_COUNTRY = 'COL'
    BRAZIL_COUNTRY = 'BRA'
    COUNTRY_CHOICES = (
        (COLOMBIA_COUNTRY, u'Colombia'),
        (BRAZIL_COUNTRY, u'Brasil'),
    )
    country_of_birth = models.CharField(
        max_length=4,
        choices=COUNTRY_CHOICES,
        blank=False,
        verbose_name='País de nacimiento'
    )



    is_administrative = models.BooleanField(
        default=False,
        verbose_name='Administrativo',
        help_text='Usuario con perfil administrativo'
    )

    is_student = models.BooleanField(
        default=False,
        verbose_name='Estudiante',
        help_text='Usuario con perfil de estudiante'
    )

    is_professor = models.BooleanField(
        default=False,
        verbose_name='Docente',
        help_text='Usuario con perfil de docente',
    )

    is_staff = models.BooleanField(
        default=True,
        verbose_name='Usuario parte del equipo (staff)',
        help_text='Indica si el usuario puede entrar en este sitio de administración.'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Usuario activo en el sistema',
        help_text='Indica si el usuario debe ser tratado como activo. Desmarque esta opción en lugar de '
                  'borrar la cuenta.'
    )

    # date_joined = models.DateTimeField(default=None)
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha de vinculación al sistema',
    )

    # Django's built-in User requires a username. That username is used for logging the user in.
    # we set the USERNAME_FIELD attribute to 'username' field.
    # If I will want log in with email address, I should set 'email' field here
    # The field specified by USERNAME_FIELD must be unique, so we pass the unique=True argument
    # in the username field.
    USERNAME_FIELD = 'email'

    # For management commands request the email address when createsuperuser will be executed
    # Read this http://stackoverflow.com/questions/25239164/issue-with-createsuperuser-when-implementing-custom-user-model
    REQUIRED_FIELDS = ['username', ]

    # When you want to get a model instance in Django, you use an expression of the form Model.objects.get(**kwargs).
    # The objects attribute here is a Manager class whose name typically follows the <model name>Manager convention.
    # In our case, we will create an UserManager class in managers.py file.
    # The object manager is used to make queries. Things like MyModel.objects.filter(...) sounds familiar right?
    # By defining a custom object manager, we will be able to define custom functions to make queries, like
    # MyModel.objects.get_by_start_date(). We will do this momentarily.
    objects = UserManager()

    # We redefine the attributes (create db_table attribute) in class Meta to say to Django
    # that users will save in the same table that the Django default user model
    # https://github.com/django/django/blob/master/django/contrib/auth/models.py#L343
    # The name of the database table to use for the model:
    # https://docs.djangoproject.com/en/1.9/ref/models/options/#db-table
    class Meta:
        db_table = 'auth_user'
        verbose_name_plural = 'Usuarios en el sistema de información'

    # get_full_name() and get_short_name() are Django conventions. We won't be using either of these methods,
    # but it is still a good idea to include them to comply with Django conventions.
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
        # return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    # We get the profiles user according with their type
    def get_medical_profile(self):
        medical_profile = None
        # medical_profile = MedicalProfile.objects.get(self.user.first_name)
        if hasattr(self, 'medicalprofile'):
            medical_profile = self.medicalprofile
        return medical_profile

    def get_therapist_profile(self):
        therapist_profile = None
        if hasattr(self, 'therapistprofile'):
            therapist_profile = self.therapistprofile
        return therapist_profile

    def get_patient_profile(self):
        patient_profile = None
        if hasattr(self, 'patientprofile'):
            patient_profile = self.patientprofile
        return patient_profile

    def get_levels_game(self):
        level_game = None
        if hasattr(self, 'level'):
            level_game=self.level
        return level_game
