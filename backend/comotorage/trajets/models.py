from django.db import models
# Create your models here.

class Trajet(models.Model):
    id=models.AutoField(primary_key=True)
    conducteur=models.ForeignKey('users.utilisateurs',on_delete=models.CASCADE,related_name='trajets_conduits')
    point_depart=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    date_depart=models.DateTimeField()
    sieges_dispo=models.IntegerField()
    prix=models.IntegerField()
    type_vehicule=models.CharField(max_length=50,blank=True,null=True)
    marque_vehicule=models.CharField(max_length=50,blank=True,null=True)

    #Relation avec le modele utilisateurs
    passagers=models.ManyToManyField('users.utilisateurs',blank=True,related_name='trajet_reserves')


