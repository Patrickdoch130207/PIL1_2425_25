from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class  utilisateurs(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    nom=models.CharField(max_length=100)
    prenom=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    telephone=models.CharField(max_length=15, blank=True,null=True)
    ville=models.CharField(max_length=100,blank=True,null=True)
    pays=models.CharField(max_length=100,blank=True,null=True)
    sexe=models.CharField(max_length=10,choices=[('Homme','Homme'),('Femme','Femme')],blank=True,null=True)
    photo_profil=models.ImageField(upload_to='',blank=True,null=True)

     