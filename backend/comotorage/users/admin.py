from django.contrib import admin
from .models import Utilisateur
from django.contrib.auth.admin import UserAdmin


admin.site.register(Utilisateur,UserAdmin)


# Register your models here.
