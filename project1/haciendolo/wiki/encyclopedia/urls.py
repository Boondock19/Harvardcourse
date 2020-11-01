from django.urls import path
from django import forms 
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("RandomPage", views.RandomPage, name="RandomPage"),
    path("NewEntryPage", views.NewEntry, name="NewEntryPage"),
    path("wiki/edit/<str:title>", views.EditEntry, name="EditEntry"),
    path("search", views.SearchEntry, name="search_results"),
    
]

