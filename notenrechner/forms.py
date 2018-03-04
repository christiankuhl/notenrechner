from django import forms
from notenrechner.models import Schueler, Klasse, Klausur, Aufgabe

class SchuelerForm(forms.ModelForm):
    class Meta:
        model = Schueler
        exclude = ['klassen']

class KlassenForm(forms.ModelForm):
    class Meta:
        model = Klasse
        exclude = []

class KlausurForm(forms.ModelForm):
    class Meta:
        model = Klausur
        exclude = []
    def __init__(self, *args, **kwargs):
        super(KlausurForm, self).__init__(*args, **kwargs)
        self.fields["anzahl_aufgaben"].widget.attrs["style"] = "width:70px"
        self.fields["nummer"].widget.attrs["style"] = "width:70px"

class AufgabeForm(forms.ModelForm):
    class Meta:
        model = Aufgabe
        exclude = []
