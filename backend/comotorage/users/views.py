from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import authenticate,login,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.urls import reverse_lazy
from users.models import PasswordResetCode
import random
from django.core.mail import send_mail

def accueil(request):
    return render(request, 'users/accueil.html')

def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Votre compte a été créé avec succès!')
            return redirect('connexion')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'E-mail ou mot de passe incorrect.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/connexion.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')


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

def deconnexion(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('accueil')




