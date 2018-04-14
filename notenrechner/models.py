from django.db import models
from klausur.constants import RANGES
from accounts.models import OwnedModel
from collections import OrderedDict, defaultdict
from statistics import mean, stdev as std
import klausur.util as util

class Fach(models.Model):
    name = models.CharField(max_length=20)
    def __repr__(self):
        return self.name
    __str__ = __repr__

class Klasse(OwnedModel):
    name = models.CharField(max_length=20)
    jahrgang = models.CharField(max_length=10)
    def anzahl_schueler(self):
        return len(self.schueler.all())
    def faecher(self):
        self.klausuren.values_list("fach").distinct()
    @property
    def klausurliste(self):
        result = {}
        for klausur in self.klausuren.all():
            try:
                result[klausur.fach].append(klausur)
            except:
                result[klausur.fach] = [klausur]
            for klausuren in result.values():
                klausuren.sort(key=lambda k: k.nummer)
        return result
    def __repr__(self):
        return ", ".join([self.name, self.jahrgang])
    __str__ = __repr__
    class Meta:
        unique_together = ("name", "jahrgang")

class Schueler(OwnedModel):
    vorname = models.CharField(max_length=60)
    nachname = models.CharField(max_length=60)
    zusatz = models.CharField(max_length=60, null=True, blank=True)
    klassen = models.ManyToManyField(Klasse, related_name="schueler")
    @property
    def klausurergebnisse(self):
        result = {}
        for klausur in Klausur.objects.all():
            try:
                punkte = self.abgaben.get(klausur=klausur).punkte()
                note = self.abgaben.get(klausur=klausur).note()
            except:
                punkte = "-"
                note = "-"
            result[klausur] = "{} / {}".format(punkte, note)
        return result
    def __repr__(self):
        result = ", ".join([self.nachname, self.vorname])
        if self.zusatz:
            result += " {}".format(self.zusatz)
        return result
    __str__ = __repr__
    class Meta:
        unique_together = ("vorname", "nachname", "zusatz")
        ordering = ('nachname', )

class Klausur(OwnedModel):
    klasse = models.ForeignKey(Klasse, related_name="klausuren", null=True, on_delete=models.SET_NULL)
    fach = models.ForeignKey(Fach, related_name="+", null=True, on_delete=models.SET_NULL)
    nummer = models.PositiveSmallIntegerField()
    titel = models.CharField(max_length=100)
    anzahl_aufgaben = models.PositiveSmallIntegerField(default=3, verbose_name="Aufgaben")
    def total(self):
        return sum(a.max_punkte for a in self.aufgaben.all())
    def anzahl_abgaben(self):
        return len(self.abgaben.all())
    def notenspiegel(self):
        result = OrderedDict({n: 0 for n in range(16)})
        for abgabe in self.abgaben.all():
            result[abgabe.note()] += 1
        return result
    def durchschnitt(self):
        return round(mean([a.note() for a in self.abgaben.all()]), 2)
    def standardabweichung(self):
        return round(std([a.note() for a in self.abgaben.all()]), 2)
    def _range(self, n):
        r = [p/2 for p in range(2*round(self.total()) + 1) if util.note(float(p/(2*self.total()))) == n]
        if r:
            return [min(r), max(r)]
        else:
            return ["-", "-"]
    def kriterien(self):
        return OrderedDict({n: self._range(n) for n in range(16)})
    def zulaessig(self):
        return len([a for a in self.abgaben.all() if a.note() < 5]) <= self.anzahl_abgaben()/2
    def beste_boese(self):
        boese = [a for a in self.abgaben.all() if a.note() < 5]
        boese.sort(key=lambda a: a.punkte(), reverse=True)
        return boese[:round(self.anzahl_abgaben()/2)-len(boese)]
    def teilnehmer(self):
        schueler_ids = self.abgaben.all().values_list('schueler', flat=True)
        return Schueler.objects.filter(pk__in=schueler_ids)
    class Meta:
        unique_together = ("fach", "klasse", "nummer")

class Aufgabe(OwnedModel):
    klausur = models.ForeignKey(Klausur, related_name="aufgaben", on_delete=models.CASCADE)
    nummer = models.PositiveSmallIntegerField()
    max_punkte = models.DecimalField(decimal_places=1, max_digits=4, default=10, null=True)
    class Meta:
        unique_together = ("klausur", "nummer")

class Abgabe(OwnedModel):
    klausur = models.ForeignKey(Klausur, related_name="abgaben", on_delete=models.CASCADE)
    schueler = models.ForeignKey(Schueler, related_name="abgaben", on_delete=models.CASCADE)
    def punkte(self):
        return sum(a.punkte for a in self.aufgaben.all())
    def note(self):
        percentage = float(round(self.punkte()/self.klausur.total(), 2))
        note = util.note(percentage)
        return note
    class Meta:
        unique_together = ("klausur", "schueler")

class AufgabenAbgabe(OwnedModel):
    abgabe = models.ForeignKey(Abgabe, related_name="aufgaben", on_delete=models.CASCADE)
    aufgabe = models.ForeignKey(Aufgabe, on_delete=models.CASCADE)
    punkte = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    class Meta:
        unique_together = ("abgabe", "aufgabe")
