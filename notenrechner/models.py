from django.db import models

class Fach(models.Model):
    name = models.CharField(max_length=20)

class Klasse(models.Model):
    name = models.CharField(max_length=20)
    jahrgang = models.CharField(max_length=10)

class Schueler(models.Model):
    vorname = models.CharField(max_length=60)
    nachname = models.CharField(max_length=60)
    klasse = models.ManyToManyField(Klasse, related_name="schueler")

class Klausur(models.Model):
    klasse = models.ForeignKey(Klasse, related_name="klausuren", null=True, on_delete=models.SET_NULL)
    fach = models.ForeignKey(Fach, related_name="+", null=True, on_delete=models.SET_NULL)
    titel = models.CharField(max_length=100)
    nummer = models.PositiveSmallIntegerField()
    anzahl_aufgaben = models.IntegerField(default=3)

class Aufgabe(models.Model):
    klausur = models.ForeignKey(Klausur, related_name="aufgaben", on_delete=models.CASCADE)
    aufgabe = models.PositiveSmallIntegerField()
    max_punkte = models.DecimalField(decimal_places=1, max_digits=4)

class Abgabe(models.Model):
    klausur = models.ForeignKey(Klausur, related_name="abgaben", on_delete=models.CASCADE)
    schueler = models.ForeignKey(Schueler, related_name="abgaben", on_delete=models.CASCADE)

class AufgabenAbgabe(models.Model):
    abgabe = models.ForeignKey(Abgabe, related_name="aufgaben", on_delete=models.CASCADE)
    aufgabe = models.PositiveSmallIntegerField()
    punkte = models.DecimalField(decimal_places=1, max_digits=4)
