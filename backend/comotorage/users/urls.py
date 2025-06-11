from django.contrib import admin
from django.urls import path
from users import views

urlpatterns=[
    path('',views.accueil,name='accueil'),
    path('inscription/',views.inscription,name='inscription'),
    path('dashboard/',views.dashboard,name='dashboard'),
]