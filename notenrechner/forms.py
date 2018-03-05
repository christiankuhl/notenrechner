from django import forms
from notenrechner.models import Schueler, Klasse, Klausur, Aufgabe, Abgabe, AufgabenAbgabe

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

class AufgabenForm(forms.Form):
    def __init__(self, klausur=None, create_abgabe=False, initial=None, data=None, *args, **kwargs):
        self.klausur = klausur
        self.create_abgabe = create_abgabe
        self.data = {}
        if not self.create_abgabe:
            for aufg in klausur.aufgaben.all():
                field_id = "aufgabe_{}".format(aufg.nummer)
                self.data[field_id] = aufg.max_punkte
        if initial:
            for field_id, value in initial.items():
                self.data[field_id] = value
        if data:
            for field_id, value in data.items():
                if self.create_abgabe and field_id[:4] == "form":
                    field_id = field_id.split("-")[-1]
                elif self.create_abgabe and field_id[:4] != "form":
                    continue
                self.data[field_id] = value
        super(AufgabenForm, self).__init__(self.data, initial, *args, **kwargs)
        if self.create_abgabe:
            self.fields["schueler"] = forms.ModelChoiceField(self.klausur.klasse.schueler.all(),
                                                             label="", required=False)
        for nummer in range(1, klausur.anzahl_aufgaben+1):
            if self.create_abgabe:
                label = ""
            else:
                label = "Aufgabe {}".format(nummer)
            value = self.data.get(label)
            field_id = 'aufgabe_{}'.format(nummer)
            self.fields[field_id] = forms.DecimalField(decimal_places=1,
                                                       max_digits=4,
                                                       min_value=0,
                                                       initial=value,
                                                       label=label,
                                                       required=False)
            self.fields[field_id].widget.attrs["step"] = .5
    def save(self):
        schueler = Schueler.objects.get(pk=1)#self.data["schueler"])
        for field_id, value in self.data.items():
            if field_id[:7] == "aufgabe":
                nummer = int(field_id.split("_")[1])
                aufgabe, _ = Aufgabe.objects.get_or_create(klausur=self.klausur,
                                                           nummer=nummer)
                if not self.create_abgabe:
                    aufgabe.max_punkte = value
                    aufgabe.save()
                else:
                    abgabe, _ = Abgabe.objects.get_or_create(klausur=self.klausur,
                                                             schueler=schueler)
                    aufgabenabgabe, _ = AufgabenAbgabe.objects.get_or_create(abgabe=abgabe,
                                                                          aufgabe=aufgabe)
                    aufgabenabgabe.punkte = value
                    aufgabenabgabe.save()
