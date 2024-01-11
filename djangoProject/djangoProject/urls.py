"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pokemonend import  views

urlpatterns = [
    path('', views.index, name='home'),
    path('pokemonend/', views.index,name='index'),
    path('pokemonend/about/',views.about,name='about'),
    path('pokemonend/work/', views.work,name='work'),

    path('pokemonend/cost/', views.cost,name='cost'),
    path('pokemonend/contact/', views.pokemon_contact,name='contact'),
    path('pokemonend/credits/', views.pokemon_credits,name='credits'),


]

