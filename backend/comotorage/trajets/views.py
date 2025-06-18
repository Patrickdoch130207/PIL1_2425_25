from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from trajets.models import Trajet, DemandeTrajet, Reservation
from django.contrib.auth import login
from django.contrib import messages
from users.models import Utilisateur
from .utils.geocoding import geocode
from .utils.osrm import get_osrm_route_info
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

# Création de trajets par les conducteurs
@login_required
def creer_trajet(request):
    if request.method == 'POST':
        point_depart = request.POST.get('depart')
        destination = request.POST.get('destination')
        date_depart = request.POST.get('date')
        heure_depart = request.POST.get('heure')
        sieges_dispo = request.POST.get('sieges_dispo')
        conducteur = request.user

        if point_depart and destination and date_depart and heure_depart:
            lat_dep, lon_dep = geocode(point_depart)
            lat_dest, lon_dest = geocode(destination)
            if None in (lat_dep, lon_dep, lat_dest, lon_dest):
                messages.error(request, "Impossible de localiser une des adresses. Vérifiez les noms de lieux.")
                return render(request, 'trajets/trajet_propose.html')

            Trajet.objects.create(
                point_depart=point_depart,
                destination=destination,
                date_depart=date_depart,
                heure_depart=heure_depart,
                sieges_dispo=sieges_dispo,
                conducteur=conducteur,
                depart_latitude=lat_dep,
                depart_longitude=lon_dep,
                dest_latitude=lat_dest,
                dest_longitude=lon_dest
            )
            messages.success(request, "Votre trajet a été publié !")
            return redirect('trajets:liste_trajets')
        else:
            messages.error(request, "Veuillez remplir tous les champs.")

    return render(request, 'trajets/trajet_propose.html')

# Liste des trajets
@login_required
def liste_trajets(request):
    utilisateur = request.user
    trajets = Trajet.objects.filter(conducteur=utilisateur)
    return render(request, 'trajets/liste_trajets.html', {'trajets': trajets})

@login_required
def liste_demande_trajet(request):
    utilisateur = request.user
    demandes = DemandeTrajet.objects.filter(passager=utilisateur)
    return render(request, 'trajets/liste_demande_trajet.html', {'demandes': demandes})

@login_required
def detail_trajet(request, id):
    trajet = get_object_or_404(Trajet, id=id)
    return render(request, 'trajets/detail_trajet.html', {'trajets': trajet})

# Suppression de trajets
@login_required
def supprimer_trajet(request, id):
    trajet = get_object_or_404(Trajet, id=id)
    trajet.delete()
    return redirect('trajets:liste_trajets')

@login_required
def supprimer_demande_trajet(request, id):
    demande = get_object_or_404(DemandeTrajet, id=id)
    demande.delete()
    return redirect('trajets:liste_demande_trajet')

# Demande de trajet par les passagers
@login_required
def creer_demande_trajet(request):
    if request.method == 'POST':
        point_depart = request.POST.get('depart')
        destination = request.POST.get('destination')
        date_depart = request.POST.get('date')
        heure_depart = request.POST.get('heure')
        if point_depart and destination and date_depart and heure_depart:
            lat_dep, lon_dep = geocode(point_depart)
            lat_dest, lon_dest = geocode(destination)

            if None in (lat_dep, lon_dep, lat_dest, lon_dest):
                messages.error(request, "Impossible de localiser une des adresses. Vérifiez les noms de lieux.")
                return render(request, 'trajets/trajet_demande.html')

            DemandeTrajet.objects.create(
                passager=request.user,
                point_depart=point_depart,
                destination=destination,
                date_depart=date_depart,
                heure_depart=heure_depart,
                depart_latitude=lat_dep,
                depart_longitude=lon_dep,
                dest_latitude=lat_dest,
                dest_longitude=lon_dest
            )
            messages.success(request, "Votre demande de trajet a été créée avec succès !")
            return redirect('trajets:liste_demande_trajet')
        else:
            messages.error(request, "Veuillez remplir tous les champs.")

    return render(request, 'trajets/trajet_demande.html')

# Réservation de trajets
@login_required
def reserver_trajet(request, trajet_id):
    trajet = get_object_or_404(Trajet, id=trajet_id)
    utilisateur = request.user
    if utilisateur in trajet.passagers.all():
        messages.info(request, 'Vous avez déjà réservé ce trajet.')

    if Reservation.objects.filter(trajet=trajet, passager=utilisateur).exists():
        messages.info(request, 'Vous avez déjà fait une demande pour ce trajet.')
    elif trajet.est_complet():
        messages.error(request, "Ce trajet n'accepte plus de nouvelles demandes.")
    else:
        Reservation.objects.create(trajet=trajet, passager=utilisateur)
        messages.success(request, "Demande envoyée. En attente de confirmation du conducteur.")

    return redirect('trajets:liste_demande_trajet')

@login_required
def mes_reservations(request):
    utilisateur = request.user
    reservations = Reservation.objects.filter(passager=utilisateur, statut='acceptee')

    return render(request, 'trajets/mes_reservations.html', {
        'reservations': reservations
    })

@login_required
def annuler_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    utilisateur = request.user

    if reservation.passager == utilisateur and reservation.statut == 'acceptee':
        reservation.delete()
        messages.success(request, "Votre réservation a été annulée.")
    else:
        messages.warning(request, "Impossible d'annuler cette réservation.")

    return redirect('trajets:mes_reservations')

@login_required
def gerer_reservations(request):
    utilisateur = request.user
    trajets = Trajet.objects.filter(conducteur=utilisateur)
    demandes = Reservation.objects.filter(trajet__in=trajets, statut='en_attente')

    return render(request, 'trajets/gerer_reservations.html', {
        'demandes': demandes
    })

@login_required
def traiter_reservation(request, reservation_id, action):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.trajet.conducteur != request.user:
        messages.error(request, "Action non autorisée.")
        return redirect('trajets:gerer_reservations')

    if action == 'accepter':
        if reservation.trajet.sieges_dispo > reservation.trajet.reservations.filter(statut='acceptee').count():
            reservation.statut = 'acceptee'
            reservation.save()
            messages.success(request, "Réservation acceptée.")
        else:
            messages.warning(request, "Plus de sièges disponibles.")
    elif action == 'refuser':
        reservation.statut = 'refusee'
        reservation.save()
        messages.info(request, "Réservation refusée.")

    return redirect('trajets:gerer_reservations')

# Modifier une proposition de trajet 
@login_required
def modifier_trajet_propose(request, id):
    trajet = get_object_or_404(Trajet, id=id)
    conducteur = request.user

    # S'assurer que seul le conducteur du trajet peut modifier
    if trajet.conducteur != conducteur:
        messages.error(request, "Vous n’êtes pas autorisé à modifier ce trajet.")
        return redirect('trajets:liste_trajets')

    if request.method == 'POST':
        depart = request.POST.get('depart')
        destination = request.POST.get('destination')
        date_depart = request.POST.get('date')
        heure_depart = request.POST.get('heure')
        sieges_dispo = request.POST.get('sieges_dispo')

        if depart and destination and date_depart and heure_depart:
            lat_dep, lon_dep = geocode(depart)
            lat_dest, lon_dest = geocode(destination)
            if None in (lat_dep, lon_dep, lat_dest, lon_dest):
                messages.error(request, "Impossible de localiser une des adresses. Vérifiez les noms de lieux.")
                return render(request, 'trajets/modifier_trajet_propose.html')

            trajet.point_depart = depart
            trajet.destination = destination
            trajet.date_depart = date_depart
            trajet.heure_depart = heure_depart
            trajet.sieges_dispo = sieges_dispo
            trajet.depart_latitude = lat_dep
            trajet.depart_longitude = lon_dep
            trajet.dest_latitude = lat_dest
            trajet.dest_longitude = lon_dest
            trajet.save()
            messages.success(request, "Le trajet a été modifié avec succès.")
            return redirect('trajets:liste_trajets')
        else:
            messages.error(request, "Tous les champs doivent être remplis.")

    return render(request, 'trajets/modifier_trajet_propose.html', {'trajet': trajet})

# Modification trajet côté passager
@login_required
def modifier_demande_trajet(request, id):
    demande = get_object_or_404(DemandeTrajet, id=id)
    passager = request.user

    # Vérifier si le passager est bien l’auteur de la demande
    if demande.passager != passager:
        messages.error(request, "Vous n’êtes pas autorisé à modifier cette demande.")
        return redirect('trajets:liste_trajets')

    if request.method == 'POST':
        depart = request.POST.get('depart')
        destination = request.POST.get('destination')
        date_depart = request.POST.get('date')
        heure_depart = request.POST.get('heure')

        if depart and destination and date_depart and heure_depart:
            lat_dep, lon_dep = geocode(depart)
            lat_dest, lon_dest = geocode(destination)
            if None in (lat_dep, lon_dep, lat_dest, lon_dest):
                messages.error(request, "Impossible de localiser une des adresses. Vérifiez les noms de lieux.")
                return render(request, 'trajets/modifier_trajet_propose.html')

            demande.point_depart = depart
            demande.destination = destination
            demande.date_depart = date_depart
            demande.heure_depart = heure_depart
            demande.depart_latitude = lat_dep
            demande.depart_longitude = lon_dep
            demande.dest_latitude = lat_dest
            demande.dest_longitude = lon_dest
            demande.save()
            messages.success(request, "Votre demande a été mise à jour.")
            return redirect('trajets:liste_demande_trajet')
        else:
            messages.error(request, "Tous les champs sont requis.")

    return render(request, 'trajets/modifier_demande_trajet.html', {'demande': demande})

# Algorithme de matching
@login_required
def matching_trajets(request, id):
    demande = get_object_or_404(DemandeTrajet, id=id)
    utilisateur = request.user

    # Geocodage
    if not demande.depart_latitude or not demande.depart_longitude:
        demande.depart_latitude, demande.depart_longitude = geocode(demande.point_depart)
    if not demande.dest_latitude or not demande.dest_longitude:
        demande.dest_latitude, demande.dest_longitude = geocode(demande.destination)

    correspondances = []
    trajets = Trajet.objects.exclude(conducteur=utilisateur).filter(
        sieges_dispo__gt=0,
        date_depart=demande.date_depart
    )

    for trajet in trajets:
        if not trajet.depart_latitude or not trajet.depart_longitude:
            trajet.depart_latitude, trajet.depart_longitude = geocode(trajet.point_depart)
        if not trajet.dest_latitude or not trajet.dest_longitude:
            trajet.dest_latitude, trajet.dest_longitude = geocode(trajet.destination)

        route_dep = get_osrm_route_info(
            demande.depart_longitude, demande.depart_latitude,
            trajet.depart_longitude, trajet.depart_latitude
        )
        route_dest = get_osrm_route_info(
            demande.dest_longitude, demande.dest_latitude,
            trajet.dest_longitude, trajet.dest_latitude
        )

        if route_dep and route_dest:
            if route_dep["distance_km"] < 5 and route_dest["distance_km"] < 5:
                # Vérifie que les horaires sont à +/- 30 min près
                delta = abs(datetime.combine(trajet.date_depart, trajet.heure_depart) -
                            datetime.combine(demande.date_depart, demande.heure_depart))
                if delta <= timedelta(minutes=30):
                    correspondances.append({
                        "trajet": trajet,
                        "distance_depart": round(route_dep["distance_km"], 2),
                        "distance_arrivee": round(route_dest["distance_km"], 2),
                        "delta_horaire_min": int(delta.total_seconds() // 60)
                    })

    return render(request, 'trajets/resultats_matching.html', {
        "demande": demande,
        "correspondances": correspondances
    })