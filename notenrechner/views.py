from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from notenrechner.models import Klasse, Schueler, Klausur, Aufgabe
from notenrechner.forms import KlassenForm, SchuelerForm, KlausurForm, AufgabenForm#, AufgabenInlineFormSet
from django.forms import formset_factory

@login_required
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

@login_required
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

@login_required
def view_klausur(request, klausur_id):
    klausur = get_object_or_404(Klausur, pk=klausur_id)
    AufgabenFormSet = formset_factory(AufgabenForm)
    initial = [{**{"schueler": abg.schueler},
                **{"aufgabe_{}".format(a.aufgabe.nummer): a.punkte
                                for a in abg.aufgaben.all()}}
                                    for abg in klausur.abgaben.all()]
    if request.method == "POST":
        form = AufgabenForm(klausur, data=request.POST)
        formset =  AufgabenFormSet(initial=initial,
                                   data=request.POST,
                                   form_kwargs={"klausur": klausur,
                                                "create_abgabe": True})
        # if form.is_valid():
        #     form.save()
        if formset.is_valid():
            for aufg_form in formset:
                aufg_form.save()
    else:
        form = AufgabenForm(klausur)
        formset = AufgabenFormSet(initial=initial, form_kwargs={"klausur": klausur, "create_abgabe": True})
    # return HttpResponse(formset)
    return render(request, "notenrechner/klausur.html", {"form": form,
                                                         "formset": formset})

@login_required
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
