from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def enter_klausur(request, form):
    pass

def klassen(request):
    return HttpResponse("Hello, world!")

def klausur(request):
    return HttpResponse("Hello, world!")

def index(request):
    if not request.user.is_authenticated:
        greeting = " zur Klausur-App"
    else:
        greeting = ", {}".format(request.user.first_name)
    return render(request, "notenrechner/index.html", {"greeting": greeting})

@login_required
def overview(request):
    return HttpResponse("Hello, world!")
