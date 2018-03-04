from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from notenrechner.models import Klasse, Schueler, Klausur, Aufgabe
from notenrechner.forms import KlassenForm, SchuelerForm, KlausurForm, AufgabeForm
from django.forms.models import inlineformset_factory

def enter_klausur(request, form):
    pass

def view_klasse(request, klassen_id):
    klasse = get_object_or_404(Klasse, pk=klassen_id)
    title = "Klasse {}, {}".format(klasse.name, klasse.jahrgang)
    if request.method == "POST":
        form = SchuelerForm(request.POST)
        if form.is_valid():
            schueler, created = Schueler.objects.get_or_create(**form.cleaned_data)
            schueler.klassen.add(klassen_id)
            schueler.save()
            return redirect("notenrechner:klasse", klassen_id=klasse.id)
        else:
            return render(request, "notenrechner/klasse.html",
                          {"form": form,
                           "content_title": title,
                           "klasse": klasse})
    else:
        return render(request, "notenrechner/klasse.html",
                      {"form": SchuelerForm(),
                       "content_title": title,
                       "klasse": klasse})

def view_klassen(request):
    klassen = Klasse.objects.all()
    if request.method == "POST":
        form = KlassenForm(request.POST)
        if form.is_valid():
            klasse = form.save()
            return redirect("notenrechner:klasse", klassen_id=klasse.id)
        else:
            return render(request, "notenrechner/klassen.html",
                          {"form": form,
                           "content_title": "Klassen",
                           "klassen": klassen})
    else:
        return render(request, "notenrechner/klassen.html",
                      {"form": KlassenForm(),
                       "content_title": "Klassen",
                       "klassen": klassen})

def view_klausur(request, klausur_id):
    klausur = get_object_or_404(Klausur, pk=klausur_id)
    AufgabenFormSet = inlineformset_factory(Klausur, Aufgabe, exclude=[],
                                            can_delete=False, extra=10,
                                            max_num=klausur.anzahl_aufgaben)
    formset = AufgabenFormSet(instance=klausur)
    if request.method == "POST":
        formset = AufgabenFormSet(request.POST, instance=klausur)
        if formset.is_valid():
            formset.save()
        return render(request, "notenrechner/klausur.html",
                      {"form": formset})
    else:
        return render(request, "notenrechner/klausur.html",
                  {"form": formset})

def view_klausuren(request):
    klausuren = Klausur.objects.all()
    if request.method == "POST":
        form = KlausurForm(request.POST)
        if form.is_valid():
            klausur = form.save()
            return redirect("notenrechner:klausur", klausur_id=klausur.id)
        else:
            return render(request, "notenrechner/klausuren.html",
                          {"form": form,
                           "content_title": "Klausuren",
                           "klausuren": klausuren})
    else:
        return render(request, "notenrechner/klausuren.html",
                      {"form": KlausurForm,
                       "content_title": "Klausuren",
                       "klausuren": klausuren})

def index(request):
    if not request.user.is_authenticated:
        greeting = " zur Klausur-App"
    else:
        greeting = ", {}".format(request.user.first_name)
    return render(request, "notenrechner/index.html", {"greeting": greeting})

@login_required
def overview(request):
    return HttpResponse("Hello, world!")
