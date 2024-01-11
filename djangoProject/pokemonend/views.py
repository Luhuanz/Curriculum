from django.shortcuts import render,HttpResponse
import os

# Create your views here.
def index(request):
    return render(request,"index.html")
def about(request):
    return render(request,"pages/about.html")
def  work(request):
    return render(request,"pages/work.html")

def  cost(request):
    return render(request, "pages/cost.html")

def  pokemon_contact(request):
    return render(request, "pages/contact.html")

def  pokemon_credits(request):

    return render(request, "pages/credits.html")
if __name__ == '__main__':
    pass
