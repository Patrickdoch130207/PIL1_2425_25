from django.db import models
from django.contrib.auth.models import AbstractUser
import random

# Create your models here.

class  Utilisateur(AbstractUser):
    id=models.AutoField(primary_key=True)
    nom=models.CharField(max_length=100)
    prenom=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=255,blank=False,null=False,default='temporary_password')
    telephone=models.CharField(max_length=15, blank=True,null=True)
    ville=models.CharField(max_length=100,blank=True,null=True)
    pays=models.CharField(max_length=100,blank=True,null=True)
    sexe=models.CharField(max_length=10,choices=[('Homme','Homme'),('Femme','Femme')],blank=True,null=True)
    photo_profil = models.ImageField(upload_to='photos_profil/',blank=True,null=True, default='photos_profil/profile_defaut.png'  
    )
    role = models.CharField(max_length=20, choices=[('Passager', 'passager'), ('Conducteur', 'conducteur')],blank=True,null=True )
    profil_complet = models.BooleanField(default=False)

        # Utiliser l'email comme identifiant de connexion
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"



class PasswordResetCode(models.Model):
    user=models.OneToOneField(Utilisateur,on_delete=models.CASCADE)
    code=models.CharField(max_length=6)
    created_at=models.DateTimeField(auto_now_add=True)

    def generate_code(self):
        self.code=str(random.randint(100000,999999))
        





