from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from trajets.models import Trajet


# Create your views here.

#Creation de trajets

def creer_trajet(request):
    if request.method=='POST':
        point_depart=request.POST.get('depart')
        destination=request.POST.get('destination')
        date_depart=request.POST.get('date')
        heure_depart=request.POST.get('heure')
        conducteur=request.user

    if point_depart and destination and date_depart and heure_depart:
        Trajet.objects.create(
            point_depart=point_depart,
           destination=destination,
           date_depart=date_depart,
           heure_depart=heure_depart,
           conducteur=conducteur 
        )
        return redirect('liste_trajets')
    
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