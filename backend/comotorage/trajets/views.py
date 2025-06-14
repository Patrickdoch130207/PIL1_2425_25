from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from trajets.models import Trajet
from django.contrib.auth import login
from django.contrib import messages


# Create your views here.

#Creation de trajets par les conducteurs

def creer_trajet(request):
    if request.method=='POST':
        point_depart=request.POST.get('depart')
        destination=request.POST.get('destination')
        date_depart=request.POST.get('date')
        heure_depart=request.POST.get('heure')
        sieges_dispo=request.POST.get('sieges_dispo')
        conducteur=request.user

    if point_depart and destination and date_depart and heure_depart:
        Trajet.objects.create(
            point_depart=point_depart,
           destination=destination,
           date_depart=date_depart,
           heure_depart=heure_depart,
           sieges_dispo=sieges_dispo,
           conducteur=conducteur 
        )
        return redirect('liste_trajets')
    return render(request,'trajets/trajet_propose.html')
    
#Liste des trajets 

def liste_trajets(request):
    trajets=Trajet.objects.all()
    return render(request,'trajets/liste_trajets.html',{'trajets':trajets})

def detail_trajet(request,id):
    trajet=get_object_or_404(Trajet,id=id)
    return render(request,'trajets/detail_trajet.html',{'trajets':trajet})

#Suppression de trajets

def supprimer_trajet(request,id):
    trajet=get_object_or_404(Trajet,id=id)
    trajet.delete()
    return redirect ('liste_trajets')

#Demande de trajet par les passagers

from trajets.models import DemandeTrajet

def creer_demande_trajet(request):
    if request.method=='POST':
        point_depart=request.POST.get('depart')
        destination=request.POST.get('destination')
        date_depart=request.POST.get('date')
        heure_depart=request.POST.get('heure')
        if point_depart and destination and date_depart and heure_depart:
            DemandeTrajet.objects.create(
                passager=request.user,
                point_depart=point_depart,
                destination=destination,
                date_depart=date_depart,
                heure_depart=heure_depart
            )
            messages.success(request, "Votre demande de trajet a été créée avec succès !")
            return redirect('home') 
        else:
            messages.error(request, "Veuillez remplir tous les champs.")
            return redirect('creer_demande_trajet')

    return render(request,'users/trajet_propose.html')



#Debut de l'algorithme de matching

#Fonction pour convertir les adresses en longitude/latitude

import googlemaps
from django.conf import settings

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

def obtenir_coordonnees(adresse):
    """ Convertit une adresse en coordonnées GPS via Google Maps API """
    geocode_result = gmaps.geocode(adresse)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None

#Algorithme de matching

def comparer_adresses(adresse1, adresse2):
    """ Vérifie si deux adresses appartiennent à la même ville/quartier """
    return adresse1.lower().strip() == adresse2.lower().strip()

def calculer_distance_google(start_coords, end_coords):
    """ Utilise Google Maps API pour obtenir la distance routière. """
    directions = gmaps.directions(start_coords, end_coords, mode="driving")
    return directions[0]['legs'][0]['distance']['value'] / 1000 if directions else None

def estimer_distance(adresse_depart, adresse_arrivee):
    """ Estime la distance si aucune coordonnée GPS n'est disponible """
    distances_connues = {
        ("Cotonou", "Abomey-Calavi"): 15,  
    }
    return distances_connues.get((adresse_depart, adresse_arrivee), 100)  # Valeur par défaut

def trouver_matching():
    demandes = DemandeTrajet.objects.filter(statut="en_attente")
    conducteurs = Trajet.objects.filter(sieges_dispo__gt=0)

    correspondances = []

    for demande in demandes:
        for trajet in conducteurs:
            # Vérification des dates et horaires
            if demande.date_depart == trajet.date_depart and demande.heure_depart == trajet.heure_depart:
                
                # Tentative de récupération des distances via Google Maps API
                if demande.latitude_depart and demande.longitude_depart and trajet.latitude_depart and trajet.longitude_depart:
                    distance = calculer_distance_google(
                        f"{demande.latitude_depart}, {demande.longitude_depart}",
                        f"{trajet.latitude_depart}, {trajet.longitude_depart}"
                    )
                else:
                    distance = estimer_distance(demande.point_depart, trajet.point_depart)  # Distance approximative

                if distance and distance < 10:  # Seuil de distance acceptable
                    score_matching = 100 - (distance * 5)  # Score basé sur la proximité
                    
                    # Vérification des préférences
                    for key in demande.preferences:
                        if trajet.preferences.get(key) != demande.preferences.get(key):
                            score_matching -= 10  # Pénalité si préférences incompatibles
                    
                    correspondances.append((demande, trajet, score_matching))

    # Trier les correspondances par **score décroissant**
    correspondances.sort(key=lambda x: x[2], reverse=True)

    return correspondances

