from django.db import models
from django.conf import settings

class Trajet(models.Model):
<<<<<<< HEAD
    id=models.AutoField(primary_key=True)
    conducteur=models.ForeignKey('users.utilisateurs',on_delete=models.CASCADE,related_name='trajets_conduits')
    point_depart=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    date_depart=models.DateField()
    heure_depart=models.TimeField()
    sieges_dispo=models.IntegerField()
    prix=models.IntegerField()
    type_vehicule=models.CharField(max_length=50,blank=True,null=True)
    marque_vehicule=models.CharField(max_length=50,blank=True,null=True)

    #Relation avec le modele utilisateurs
    passagers=models.ManyToManyField('users.utilisateurs',blank=True,related_name='trajet_reserves')

=======
    # Utilisez settings.AUTH_USER_MODEL au lieu de 'users.utilisateurs'
    conducteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trajets_conduits'
    )
    
    passagers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Trajet_passagers',
        related_name='trajets_passagers',
        blank=True
    )
    
    # Ajoutez vos autres champs ici
    # depart = models.CharField(max_length=100)
    # arrivee = models.CharField(max_length=100)
    # date_depart = models.DateTimeField()
    # prix = models.DecimalField(max_digits=6, decimal_places=2)
    # places_disponibles = models.IntegerField()
    
    def __str__(self):
        return f"Trajet par {self.conducteur}"
>>>>>>> eb56f2b (Finalisation de l'authentification)

class Trajet_passagers(models.Model):
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)
    # Utilisez settings.AUTH_USER_MODEL au lieu de 'users.utilisateurs'
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date_reservation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('trajet', 'utilisateur')