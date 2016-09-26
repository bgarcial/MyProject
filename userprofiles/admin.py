from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# http://stackoverflow.com/questions/15514912/django-admin-not-hashing-custom-user-password

from .models import (User,)
from .forms import CustomUserChangeForm, CustomUserCreationForm

# Register your models here.

# Inherit of the original UserAdmin for use the customized forms

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (
            None, {
                'fields':(
                    #'username',
                    #'password',
                    #'first_name',
                    #'last_name',
                    'age',
                    'sex',
                    #'email',
                    'photo',
                    #'is_staff',
                    #'is_active',
                    #'is_superuser',
                    #'last_login',
                    #'date_joined',

                )
            }
        ),
    )


#Change our UserAdmin class to inherit of our CustomUserAdmin created above (do not inherit of model.ModelAdmin)
@admin.register(User)
class UserAdmin(CustomUserAdmin):
    # list_display = ('photo',)


    list_display = ('username','password','first_name','last_name','age','sex',
        'photo','email','is_staff','is_active','is_superuser','last_login',)
