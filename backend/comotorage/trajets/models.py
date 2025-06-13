from django.db import models
from django.conf import settings

class Trajet(models.Model):

    id=models.AutoField(primary_key=True)
    conducteur=models.ForeignKey('users.Utilisateur',on_delete=models.CASCADE,related_name='trajets_conduits')
    point_depart=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    date_depart=models.DateField()
    heure_depart=models.TimeField()
    sieges_dispo=models.IntegerField()
    prix=models.IntegerField()
    type_vehicule=models.CharField(max_length=50,blank=True,null=True)
    marque_vehicule=models.CharField(max_length=50,blank=True,null=True)

    #Relation avec le modele utilisateurs
    passagers=models.ManyToManyField('users.Utilisateur',blank=True,related_name='trajet_reserves')



