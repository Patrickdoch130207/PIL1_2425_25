from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from trajets.models import Trajet
from django.contrib.auth import login
from django.contrib import messages
from users.models import utilisateurs


# Create your views here.

#Creation de trajets par les conducteurs

def creer_trajet(request):
    if request.method=='GET':
        point_depart=request.GET.get('depart')
        destination=request.GET.get('destination')
        date_depart=request.GET.get('date')
        heure_depart=request.GET.get('heure')
        sieges_dispo=request.GET.get('sieges_dispo')
        conducteur=utilisateurs.objects.get(user=request.user)

        if point_depart and destination and date_depart and heure_depart:
           Trajet.objects.create(
              point_depart=point_depart,
              destination=destination,
              date_depart=date_depart,
              heure_depart=heure_depart,
              sieges_dispo=sieges_dispo,
              conducteur=conducteur 
            )
           messages.success(request, "Votre demande de trajet a été créée avec succès !")
           return redirect('liste_trajets') 
        else:
           messages.error(request, "Veuillez remplir tous les champs.")
        
    return render(request,'trajets/trajet_propose.html')
    
#Liste des trajets 

def liste_trajets(request):
    trajets=Trajet.objects.all()
    return render(request,'trajets/liste_trajets.html',{'trajets':trajets})

def liste_demande_trajet(request):
    demandes=DemandeTrajet.objects.all()
    return render(request,'trajets/liste_demande_trajet.html',{'demandes':demandes})

def detail_trajet(request,id):
    trajet=get_object_or_404(Trajet,id=id)
    return render(request,'trajets/detail_trajet.html',{'trajets':trajet})

#Suppression de trajets

def supprimer_trajet(request,id):
    trajet=get_object_or_404(Trajet,id=id)
    trajet.delete()
    return redirect ('liste_trajets')

def supprimer_demande_trajet(request,id):
    demande=get_object_or_404(DemandeTrajet,id=id)
    demande.delete()
    return redirect('liste_demande_trajet')

#Demande de trajet par les passagers

from trajets.models import DemandeTrajet

def creer_demande_trajet(request):
    if request.method=='GET':
        point_depart=request.GET.get('depart')
        destination=request.GET.get('destination')
        date_depart=request.GET.get('date')
        heure_depart=request.GET.get('heure')
        if point_depart and destination and date_depart and heure_depart:
            DemandeTrajet.objects.create(
                passager=utilisateurs.objects.get(user=request.user),
                point_depart=point_depart,
                destination=destination,
                date_depart=date_depart,
                heure_depart=heure_depart
            )
            messages.success(request, "Votre demande de trajet a été créée avec succès !")
            return redirect('liste_demande_trajet') 
        else:
            messages.error(request, "Veuillez remplir tous les champs.")

    return render(request,'trajets/trajet_demande.html')

#Reservation de trajets

from django.contrib.auth.decorators import login_required
from trajets.models import Trajet

@login_required
def reserver_trajet(request, trajet_id):
    trajet = get_object_or_404(Trajet, id=trajet_id)

    # Vérifier qu’il reste des sièges
    if trajet.sieges_dispo > trajet.passagers.count():
        utilisateur = utilisateurs.objects.get(user=request.user)
        trajet.passagers.add(utilisateur)
        messages.success(request, "Vous avez réservé ce trajet avec succès.")
    else:
        messages.error(request, "Désolé, ce trajet est complet.")

    return redirect('liste_trajets')

#Modifier une demande de trajet cote conducteur
@login_required
def modifier_trajet_propose(request, id):
    trajet = get_object_or_404(Trajet, id=id)
    conducteur = utilisateurs.objects.get(user=request.user)

    # S'assurer que seul le conducteur du trajet peut modifier
    if trajet.conducteur != conducteur:
        messages.error(request, "Vous n’êtes pas autorisé à modifier ce trajet.")
        return redirect('liste_trajets')

    if request.method == 'GET':
        # Recuperation des nouvelles valeurs depuis l’URL
        depart = request.GET.get('depart')
        destination = request.GET.get('destination')
        date_depart = request.GET.get('date')
        heure_depart = request.GET.get('heure')
        sieges_dispo = request.GET.get('sieges_dispo')

        # Verifier que tous les champs requis sont présents
        if depart and destination and date_depart and heure_depart:
            trajet.point_depart = depart
            trajet.destination = destination
            trajet.date_depart = date_depart
            trajet.heure_depart = heure_depart
            trajet.sieges_dispo = sieges_dispo
            trajet.save()
            messages.success(request, "Le trajet a été modifié avec succès.")
            return redirect('liste_trajets')
        else:
            messages.error(request, "Tous les champs doivent être remplis.")

    return render(request, 'trajets/modifier_trajet_propose.html', {'trajet': trajet})

#Modification trajet cote passager

def modifier_demande_trajet(request, id):
    demande = get_object_or_404(DemandeTrajet, id=id)
    passager = utilisateurs.objects.get(user=request.user)

    # Verifier si le passager est bien l’auteur de la demande
    if demande.passager != passager:
        messages.error(request, "Vous n’êtes pas autorisé à modifier cette demande.")
        return redirect('liste_trajets')

    if request.method == 'GET':
        depart = request.GET.get('depart')
        destination = request.GET.get('destination')
        date_depart = request.GET.get('date')
        heure_depart = request.GET.get('heure')

        if depart and destination and date_depart and heure_depart:
            demande.point_depart = depart
            demande.destination = destination
            demande.date_depart = date_depart
            demande.heure_depart = heure_depart
            demande.save()
            messages.success(request, "Votre demande a été mise à jour.")
            return redirect('liste_demande_trajet')
        else:
            messages.error(request, "Tous les champs sont requis.")

    return render(request, 'trajets/modifier_demande_trajet.html', {'demande': demande})





