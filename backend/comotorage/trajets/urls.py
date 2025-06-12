from django.contrib import admin
from django.urls import path
from trajets import views

urlpatterns=[
    path('trajet_propose/',views.creer_trajet,name='creer_trajet'),
    
]