from django.db import models

class Fach(models.Model):
    name = models.CharField(max_length=20)
    def __repr__(self):
        return self.name
    __str__ = __repr__

class Klasse(models.Model):
    name = models.CharField(max_length=20)
    jahrgang = models.CharField(max_length=10)
    def anzahl_schueler(self):
        return len(self.schueler.all())
    def __repr__(self):
        return ", ".join([self.name, self.jahrgang])
    __str__ = __repr__
    class Meta:
        unique_together = ("name", "jahrgang")

class Schueler(models.Model):
    vorname = models.CharField(max_length=60)
    nachname = models.CharField(max_length=60)
    klassen = models.ManyToManyField(Klasse, related_name="schueler")
    class Meta:
        unique_together = ("vorname", "nachname")

class Klausur(models.Model):
    klasse = models.ForeignKey(Klasse, related_name="klausuren", null=True, on_delete=models.SET_NULL)
    fach = models.ForeignKey(Fach, related_name="+", null=True, on_delete=models.SET_NULL)
    nummer = models.PositiveSmallIntegerField()
    titel = models.CharField(max_length=100)
    anzahl_aufgaben = models.PositiveSmallIntegerField(default=3, verbose_name="Aufgaben")
    def anzahl_abgaben(self):
        return len(self.abgaben.all())
    class Meta:
        unique_together = ("fach", "klasse", "nummer")

class Aufgabe(models.Model):
    klausur = models.ForeignKey(Klausur, related_name="aufgaben", on_delete=models.CASCADE)
    aufgabe = models.PositiveSmallIntegerField()
    max_punkte = models.DecimalField(decimal_places=1, max_digits=4)
    class Meta:
        unique_together = ("klausur", "aufgabe")

class Abgabe(models.Model):
    klausur = models.ForeignKey(Klausur, related_name="abgaben", on_delete=models.CASCADE)
    schueler = models.ForeignKey(Schueler, related_name="abgaben", on_delete=models.CASCADE)
    class Meta:
        unique_together = ("klausur", "schueler")

class AufgabenAbgabe(models.Model):
    abgabe = models.ForeignKey(Abgabe, related_name="aufgaben", on_delete=models.CASCADE)
    aufgabe = models.PositiveSmallIntegerField()
    punkte = models.DecimalField(decimal_places=1, max_digits=4)
    class Meta:
        unique_together = ("abgabe", "aufgabe")
