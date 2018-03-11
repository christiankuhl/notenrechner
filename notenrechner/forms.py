from django import forms
from djangoformsetjs.utils import formset_media_js
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
    def save(self):
        klausur = super(KlausurForm, self).save()
        for nummer in range(1, self.cleaned_data["anzahl_aufgaben"]+1):
            aufg, created = Aufgabe.objects.get_or_create(klausur=klausur,
                                                          nummer=nummer)
            if created:
                aufg.save()
        return klausur
    class Meta:
        model = Klausur
        exclude = []
    def __init__(self, *args, **kwargs):
        super(KlausurForm, self).__init__(*args, **kwargs)
        self.fields["anzahl_aufgaben"].widget.attrs["style"] = "width:70px"
        self.fields["nummer"].widget.attrs["style"] = "width:70px"

class AufgabenForm(forms.Form):
    def __init__(self, klausur, create_abgabe=False, *args, **kwargs):
        super(AufgabenForm, self).__init__(*args, **kwargs)
        self.klausur = klausur
        initial = kwargs.get("initial")
        if create_abgabe:
            if initial:
                value = initial.get("schueler")
            else:
                value = None
            self.fields["schueler"] = forms.ModelChoiceField(self.klausur.klasse.schueler.all(),
                                                                        label="", required=False,
                                                                        initial=value)
        for aufg in klausur.aufgaben.all():
            field_id = "aufgabe_{}".format(aufg.nummer)
            if create_abgabe:
                label = ""
            else:
                label = "Aufgabe {}".format(aufg.nummer)
            if initial:
                value = initial.get(field_id)
            else:
                value = None
            self.fields[field_id] = forms.DecimalField(decimal_places=1,
                                                       max_digits=4,
                                                       min_value=0,
                                                       initial=value,
                                                       label=label,
                                                       required=False)
            self.fields[field_id].widget.attrs["step"] = .5
            self.fields[field_id].widget.attrs["style"] = "width:70px"
    def save(self):
        schueler = self.cleaned_data.get("schueler")
        for field_id, value in self.cleaned_data.items():
            if field_id[:7] == "aufgabe":
                nummer = int(field_id.split("_")[1])
                aufgabe, _ = Aufgabe.objects.get_or_create(klausur=self.klausur,
                                                           nummer=nummer)
                if not schueler:
                    aufgabe.max_punkte = value
                    aufgabe.save()
                else:
                    abgabe, _ = Abgabe.objects.get_or_create(klausur=self.klausur,
                                                             schueler=schueler)
                    aufgabenabgabe, _ = AufgabenAbgabe.objects.get_or_create(abgabe=abgabe,
                                                                          aufgabe=aufgabe)
                    aufgabenabgabe.punkte = value
                    aufgabenabgabe.save()
    class Media(object):
        js = formset_media_js

AufgabenFormSet = forms.formset_factory(AufgabenForm, can_delete=True)
AufgabenFormSet.fields["DELETE"].widget.attrs["style"] = "display:none"
