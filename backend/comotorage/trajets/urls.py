from django.contrib import admin
from django.urls import path
from trajets import views

urlpatterns=[
    path('trajet_propose/',views.creer_trajet,name='creer_trajet'),
    path('trajet_demande/', views.creer_demande_trajet, name='creer_demande_trajet'),
    path('liste_trajets/', views.liste_trajets, name='liste_trajets'),
    path('liste_demande_trajet/', views.liste_demande_trajet, name='liste_demande_trajet'),
    path('detail_trajet/<int:id>/', views.detail_trajet, name='detail_trajet'),
    path('reserver_trajet/<int:trajet_id>/', views.reserver_trajet, name='reserver_trajet'),
    path('supprimer_trajet/<int:id>/', views.supprimer_trajet, name='supprimer_trajet'),
    path('supprimer_demande_trajet/<int:id>/',views.supprimer_demande_trajet,name='supprimer_demande_trajet'),
    path('modifier_trajet_propose/<int:id>/', views.modifier_trajet_propose, name='modifier_trajet_propose'),
    path('modifier_demande_trajet/<int:id>/', views.modifier_demande_trajet, name='modifier_demande_trajet'),
]
