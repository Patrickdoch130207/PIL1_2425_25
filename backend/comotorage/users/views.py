from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .models import utilisateurs

# Create your views here.

#Gestion de la page d'accueil

def accueil(request):
    return render(request,'users/accueil.html')

#Gestion de la page home

def home(request):
    return render(request,'users/home.html')

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
        if password:
           user = User.objects.create_user(username=email, email=email, password=password)
           user.set_password(password)
           user.save()

        # Enregistrement des informations complémentaires dans le modèle utilisateurs
        user_info = utilisateurs.objects.create(
            user=user,
            nom=nom,
            prenom=prenom,
            email=email,
            telephone=telephone,
            password=user.password,
        )
        user_info.save()

        login(request, user)
        messages.success(request, "Votre inscription a bien réussi.")
        return redirect("home")  
            
    return render(request,'users/inscription.html')

#Gestion de la connexion

from django.contrib.auth import authenticate,login,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.urls import reverse_lazy
from users.models import PasswordResetCode
import random
from django.core.mail import send_mail

def connexion(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            user=User.objects.get(email=email)
            user=authenticate(request,username=user.username,password=password)
        except User.DoesNotExist:
            user=None

        if user is not None:
            login(request,user)
            messages.success(request,'Connexion reussie!')
            return redirect('home')
        else:
            messages.error(request,'Email ou mot de passe incorrect')
    return render(request,'users/connexion.html')

#Mot de passe oublie

def send_reset_code(request):
    if request.method=='POST':
        email=request.POST.get('email')

        try:
            user=User.objects.get(email=email)
            reset_code, created=PasswordResetCode.objects.get_or_create(user=user)
            reset_code.code=str(random.randint(100000,999999))
            reset_code.save()

            send_mail(
                'Code de reinitialisation',
                f'Votre code de reinitialisation est: {reset_code.code}',
                'govibe@gmail.com',
                [user.email],
                fail_silently=False,
            )

            messages.success(request,'Un code de reinitialisation a ete envoye a votre email')
            return redirect('verify_reset_code')
        except User.DoesNotExist:
            messages.error(request,'Aucun compte associe a cet email')
    return render(request,'users/mot_de_passe_oublie.html')

def verify_reset_code(request):
    if request.method=='POST':
        email=request.POST.get('email')
        code=request.POST.get('code')

        try:
            user=User.objects.get(email=email)
            reset_code=PasswordResetCode.objects.get(user=user)

            if reset_code.code==code:
                messages.success(request,'Code valide. Vous pouvez maintenant reinitialiser votre mot de passe')
                return redirect('reset_password',id=user.id)
            else:
                messages.error(request,'Code incorrect.Veuillez reesayer.')
        except(User.DoesNotExist,PasswordResetCode.DoesNotExist):
            messages.error(request,'Aucun code trouve pour cet email')
    return render(request,'users/verifier_code.html')

def reset_password(request,id):
    user=User.objects.get(User,id=id)

    if request.method=='POST':
        new_password=request.POST.get('new_password')
        confirm_password=request.POST.get('confirm_password')

        if new_password==confirm_password:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request,user)
            messages.success(request,'Votre mot de passe a ete reinitialise avec succes')
            return redirect('home')
        else:
            messages.error(request,'Les mots de passe ne correspondent pas')
    return render(request,'users/reset_password.html',{'user':user})
