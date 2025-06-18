from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Utilisateur

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ('nom', 'prenom', 'email')

class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)




class InfosPersoForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'email','telephone', 'ville', 'pays', 'sexe', 'photo_profil','role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True