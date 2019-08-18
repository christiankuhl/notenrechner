from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from notenrechner.models import Klasse, Schueler, Klausur, Aufgabe
from notenrechner.forms import KlassenForm, SchuelerForm, KlausurForm, AufgabenForm, AufgabenFormSet
from klausur.constants import APP_NAME
from accounts.models import restricted_to_owner
from django.template.defaulttags import register

@register.filter
def get(dictionary, key):
    return dictionary.get(key)

@login_required
@restricted_to_owner
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
@restricted_to_owner
def view_klassen(request):
    klassen = Klasse.objects.all()
    if request.method == "POST":
        form = KlassenForm(request.POST)
        if form.is_valid():
            klasse, created = Klasse.objects.get_or_create(**form.cleaned_data)
            klasse.save()
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
@restricted_to_owner
def view_klausur(request, klausur_id):
    klausur = get_object_or_404(Klausur, pk=klausur_id)
    initial = [{**{"schueler": abg.schueler},
                **{"aufgabe_{}".format(a.aufgabe.nummer): a.punkte
                                for a in abg.aufgaben.all()}}
                                    for abg in klausur.abgaben.all()]
    max_punkte = {"aufgabe_{}".format(a.nummer): a.max_punkte for a in klausur.aufgaben.all()}
    if request.method == "POST":
        form = AufgabenForm(klausur=klausur,
                            initial=max_punkte,
                            data=request.POST)
        formset =  AufgabenFormSet(initial=initial,
                                   data=request.POST,
                                   form_kwargs={"klausur": klausur,
                                                "create_abgabe": True})
        if form.is_valid():
            form.save()
        if formset.is_valid():
            formset.save()
        if form.is_valid() and formset.is_valid():
            return redirect("notenrechner:evaluate", klausur_id=klausur.id)
    else:
        form = AufgabenForm(klausur=klausur, initial=max_punkte)
        formset = AufgabenFormSet(initial=initial, form_kwargs={"klausur": klausur, "create_abgabe": True})
    return render(request, "notenrechner/klausur.html", {"form": form,
                                                         "formset": formset,
                                                         "klausur": klausur})

@login_required
@restricted_to_owner
def edit_klausur(request, klausur_id):
    klausur = get_object_or_404(Klausur, pk=klausur_id)
    klausuren = Klausur.objects.all()
    form = KlausurForm(request.POST or None, instance=klausur)
    if request.method == "POST":
        if form.is_valid():
            klausur = form.save()
            return redirect("notenrechner:klausur", klausur_id=klausur.id)
    return render(request, "notenrechner/klausuren.html",
                  {"form": form,
                   "form_action": "Speichern",
                   "content_title": "Klausur ändern",
                   "klausuren": klausuren})

@login_required
@restricted_to_owner
def klausur_evaluation(request, klausur_id, detail=False):
    klausur = get_object_or_404(Klausur, pk=klausur_id)
    notenspiegel = None #notenspiegel_html(klausur)
    return render(request, "notenrechner/auswertung.html", {"klausur": klausur,
                                                            "notenspiegel": notenspiegel,
                                                            "detail": detail})

@login_required
@restricted_to_owner
def klausur_detail(request, klausur_id):
    return klausur_evaluation(request, klausur_id, detail=True)

@login_required
@restricted_to_owner
def view_klausuren(request):
    klausuren = Klausur.objects.all()
    form = KlausurForm(request.POST or None, user=request.user)
    if request.method == "POST":
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
                      {"form": form,
                       "content_title": "Klausuren",
                       "klausuren": klausuren})

def index(request):
    if not request.user.is_authenticated:
        greeting = " zu {}".format(APP_NAME)
    else:
        greeting = ", {}".format(request.user.first_name)
    return render(request, "notenrechner/index.html", {"greeting": greeting})

def notenspiegel_html(klausur):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.pyplot import hist, title, xlabel, ylabel, xticks, close, figure
    import mpld3
    fig = figure(111, figsize=(4,3))
    xlabel("Note")
    ylabel("Frequenz")
    bins = [r - .5 for r in range(17)]
    xticks(range(16))
    hist([a.note() for a in klausur.abgaben.all()], bins=bins, facecolor='blue', alpha=0.5)
    canvas = FigureCanvas(fig)
    html = mpld3.fig_to_html(fig)
    return html

@login_required
@restricted_to_owner
def overview(request):
    return view_klausuren(request)

@login_required
@restricted_to_owner
def view_schueler(request, schueler_id):
    pass

@login_required
@restricted_to_owner
def edit_schueler(request, schueler_id):
    pass

@login_required
@restricted_to_owner
def delete_schueler(request, schueler_id, klassen_id=None):
    schueler = get_object_or_404(Schueler, pk=schueler_id)
    if klassen_id:
        klasse = get_object_or_404(Klasse, pk=klassen_id)
        if request.method == "GET":
            dialog_text = "Schüler {} wirklich aus der Klasse {} entfernen?".format(schueler,
                                                                                    klasse)
            return render(request, "notenrechner/dialog.html", {"dialog_heading": "Schüler entfernen?",
                                                                "dialog_text": dialog_text})
        elif request.method == "POST":
            schueler.klassen.remove(klasse)
            return redirect("notenrechner:klasse", klassen_id=klassen_id)
    else:
        if request.method == "GET":
            dialog_text = "Schüler {} wirklich löschen?".format(schueler)
            return render(request, "notenrechner/dialog.html", {"dialog_heading": "Schüler löschen?",
                                                                "dialog_text": dialog_text})
        elif request.method == "POST":
            schueler.delete()
            return redirect("notenrechner:klassen")

@login_required
@restricted_to_owner
def delete_klausur(request, klausur_id):
    klausur = get_object_or_404(Klausur, pk=klausur_id)
    if request.method == "GET":
        dialog_text = "Soll die Klausur \"{}\" ({}) wirklich gelöscht werden?".format(klausur.titel,
                                                                                 klausur.klasse)
        return render(request, "notenrechner/dialog.html", {"dialog_heading": "Klausur löschen?",
                                                            "dialog_text": dialog_text})
    elif request.method == "POST":
        klausur.delete()
        return redirect("notenrechner:klausuren")
