from django.shortcuts import render
import markdown2
from . import util
from django.http import Http404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
import random
from django import forms
from django.urls import reverse
from django.shortcuts import redirect
from django.db import models
from django.forms import ModelForm 
from .filters import SearchFilter
import re 

class NewentryForm(forms.Form):
    title=forms.CharField(label="Title",widget=forms.TextInput(attrs={'class':'form-control col-lg-5 col-md-5'}))
    contend=forms.CharField(label="Contend",widget=forms.Textarea(attrs={'class': 'form-control col-lg-5 col-md-5'}))

class EditentryForm(forms.Form):
    def __init__(self,title,contend):
        self.title=title
        self.contend=contend
        title=forms.CharField(label="Title",widget=forms.TextInput(attrs={'class':'form-control col-lg-5 col-md-5', 'value':f'{self.title}'}))
        contend=forms.CharField(label="Contend",widget=forms.Textarea(attrs={'class':'form-control col-lg-5 col-md-5','value':f'{self.contend}'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request,title):
    p=util.list_entries()
    if title not in p:
        return render (request,"encyclopedia/wiki/404.html",{
            "title":title
        })
    else:
        return render(request, "encyclopedia/wiki/entry.html", {
        "contend": markdown2.markdown(util.get_entry(title)),
        "title":title})

def RandomPage(request):
    p=util.list_entries()
    r=random.choice(p)
    return render(request, "encyclopedia/wiki/entry.html", {
    "contend": markdown2.markdown(util.get_entry(r)),
    "title":r})

def SearchEntry(request):
    if request.method == 'POST':
        term = request.POST
        term = term['q']
        #term=term[0]
        entries = util.list_entries()
        searchlist = []
        for entry in entries:
            if re.search(term.lower(), entry.lower()): 
                 searchlist.append(entry)
            
    if term in searchlist:
        return render(request, "encyclopedia/wiki/entry.html", {
            "contend": markdown2.markdown(util.get_entry(term)),
            "title":term})
    else:
        return render(request, "encyclopedia/searchbar.html", {
            'entries': searchlist
        })    

   

def NewEntry(request):
    if request.method == "POST":
        form = NewentryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            contend = form.cleaned_data["contend"]
            p=util.list_entries()
            if title in p:
                return render(request,"encyclopedia/wiki/Newentry.html",{
                    "form":form, "Error":"This Entry Already Exists"})
            util.save_entry(title,contend)
            return HttpResponseRedirect(reverse("title",kwargs={'title':f'{title}'}))
        else:
            return render(request,"encyclopedia/wiki/Newentry.html", {
                "form": form
            })       
    return render(request,"encyclopedia/wiki/Newentry.html",{
        "form":NewentryForm() 
    })

def EditEntry(request,title):
    p=util.list_entries()
    if title in p:
        contend=util.get_entry(title)
        if request.method == "POST":
            form = NewentryForm(request.POST)
            if form.is_valid():
                contend=form.cleaned_data["contend"]
                util.save_entry(title,contend)
                return HttpResponseRedirect(reverse("title",kwargs={'title':f'{title}'}))
                
        return render (request,"encyclopedia/wiki/editpage.html",{
            "title":title,"contend":contend
        })
  
   


