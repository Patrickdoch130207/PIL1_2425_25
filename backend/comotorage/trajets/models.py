from django.db import models

# Create your models here.

#Modele pour la gestion des trajets cote conducteur
class Trajet(models.Model):
    id=models.AutoField(primary_key=True)
    conducteur=models.ForeignKey('users.utilisateurs',on_delete=models.CASCADE,related_name='trajets_conduits')
    point_depart=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    date_depart=models.DateField()
    heure_depart=models.TimeField()
    latitude_depart = models.FloatField(null=True, blank=True)
    longitude_depart = models.FloatField(null=True, blank=True)
    latitude_arrivee = models.FloatField(null=True, blank=True)
    longitude_arrivee = models.FloatField(null=True, blank=True)
    date_depart = models.DateField()
    sieges_dispo=models.IntegerField()
    prix=models.IntegerField()
    type_vehicule=models.CharField(max_length=50,blank=True,null=True)
    marque_vehicule=models.CharField(max_length=50,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    preferences = models.JSONField(default=dict) 

    #Relation avec le modele utilisateurs
    passagers=models.ManyToManyField('users.utilisateurs',blank=True,related_name='trajet_reserves')


#Modele pour la gestion des trajets cote passager
from django.db import models
from django.contrib.auth.models import User

class DemandeTrajet(models.Model):
    passager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="demandes_trajet")
    point_depart = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    date_depart = models.DateField()
    heure_depart = models.TimeField()
    latitude_depart = models.FloatField(null=True, blank=True)
    longitude_depart = models.FloatField(null=True, blank=True)
    latitude_arrivee = models.FloatField(null=True, blank=True)
    longitude_arrivee = models.FloatField(null=True, blank=True)
    date_depart = models.DateField()
    statut = models.CharField(max_length=20, choices=[
        ("en_attente", "En attente"),
        ("acceptée", "Acceptée"),
        ("refusée", "Refusée"),
    ], default="en_attente")
    created_at = models.DateTimeField(auto_now_add=True)
    preferences = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.point_depart} à {self.destination}"

    