from django.db import models
from django.conf import settings
from users.models import Utilisateur

#Modele pour la gestion des trajets cote conducteur
class Trajet(models.Model):

    id=models.AutoField(primary_key=True)
    conducteur=models.ForeignKey('users.Utilisateur',on_delete=models.CASCADE,related_name='trajets_conduits')
    point_depart=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    date_depart=models.DateField()
    heure_depart=models.TimeField(auto_now=False,auto_now_add=False)
    date_depart = models.DateField()
    depart_longitude=models.FloatField(null=True)
    depart_latitude=models.FloatField(null=True)
    dest_longitude=models.FloatField(null=True)
    dest_latitude=models.FloatField(null=True)
    sieges_dispo=models.IntegerField()
    prix=models.IntegerField(null=True)
    type_vehicule=models.CharField(max_length=50,blank=True,null=True)
    marque_vehicule=models.CharField(max_length=50,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    preferences = models.JSONField(default=dict) 

    #Relation avec le modele utilisateurs
    passagers=models.ManyToManyField('users.Utilisateur',blank=True,related_name='trajet_reserves')

    def sieges_occupees(self):
        return self.reservations.filter(statut__in=['en_attente', 'acceptee']).count()

    def est_complet(self):
        return self.sieges_occupees() >= self.sieges_dispo




#Modele pour la gestion des trajets cote passager
from django.db import models
from django.contrib.auth.models import User

class DemandeTrajet(models.Model):
    passager = models.ForeignKey('users.Utilisateur', on_delete=models.CASCADE, related_name="demandes_trajet")
    point_depart = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    date_depart = models.DateField()
    heure_depart = models.TimeField(auto_now=False,auto_now_add=False)
    date_depart = models.DateField(null=False)
    depart_longitude=models.FloatField(null=True)
    depart_latitude=models.FloatField(null=True)
    dest_longitude=models.FloatField(null=True)
    dest_latitude=models.FloatField(null=True)
    statut = models.CharField(max_length=20, choices=[
        ("en_attente", "En attente"),
        ("acceptée", "Acceptée"),
        ("refusée", "Refusée"),
    ], default="en_attente")
    created_at = models.DateTimeField(auto_now_add=True)
    preferences = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.point_depart} à {self.destination}"

#Modele pour la gestion des reservations

class Reservation(models.Model):
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, related_name="reservations")
    passager = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=[
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée')
    ], default='en_attente')
    date_reservation = models.DateTimeField(auto_now_add=True)
