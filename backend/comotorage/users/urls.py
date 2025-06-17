from django.urls import path,include
from . import views

app_name = 'users'

urlpatterns = [
   
    path('', views.accueil, name='accueil'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('homepage/', views.homepage, name='homepage'),
    path('mot_de_passe_oublie/', views.send_reset_code, name='send_reset_code'),
    path('verifier_code/', views.verify_reset_code, name='verify_reset_code'),
    path('reset_password/<int:id>/', views.reset_password, name='reset_password'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
]

