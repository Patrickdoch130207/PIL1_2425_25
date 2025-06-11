from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .models import utilisateurs

# Create your views here.

#Gestion de la page d'accueil

def accueil(request):
    return render(request,'users/inscription.html')

#Gestion connexion apres inscription

# users/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, "users/dashboard.html")


#Gestion de la page d'inscription

def inscription(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Vérification des mots de passe
        if password != password_confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('inscription')

        # Vérification de l'existence de l'email
        if utilisateurs.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('inscription')

        # Création de l'utilisateur de base dans Django
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()

        # Enregistrement des informations complémentaires dans ton modèle utilisateurs
        user_info = utilisateurs.objects.create(
            user=user,
            nom=nom,
            prenom=prenom,
            email=email,
            telephone=telephone,
        )
        user_info.save()

        login(request, user)
        messages.success(request, "Votre inscription a bien réussi.")
        return redirect("dashboard")          
    return redirect('inscription')