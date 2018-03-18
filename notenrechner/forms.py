from django import forms
from django.forms.formsets import BaseFormSet, DELETION_FIELD_NAME
from djangoformsetjs.utils import formset_media_js
from notenrechner.models import Schueler, Klasse, Klausur, Aufgabe, Abgabe, AufgabenAbgabe
from collections import defaultdict

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
        self.create_abgabe = create_abgabe
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
    def clean(self):
        super(AufgabenForm, self).clean()
        if self.create_abgabe:
            if (any(p is not None for f, p in self.cleaned_data.items() if f[:7] == "aufgabe")
                                                        and not self.cleaned_data["schueler"]):
                raise forms.ValidationError("Fehler: Kein Schüler angegeben!")

    def save(self):
        schueler = self.cleaned_data.get("schueler")
        for field_id, value in self.cleaned_data.items():
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
    class Media(object):
        js = formset_media_js

class AbgabenFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        if self.can_delete:
            form.fields[DELETION_FIELD_NAME].widget.attrs["style"] = "display:none"
    def clean(self):
        if any(self.errors):
            return
        schueler = [f.cleaned_data.get("schueler") for f in self.forms
                                                     if f not in self.deleted_forms]
        tally = defaultdict(int)
        for s in schueler:
            tally[s] += 1
            if s and tally[s] > 1:
                raise forms.ValidationError("Fehler: Schüler %(schueler)s hat mehrere Abgaben!",
                                            params={"schueler": s})
    def save(self, *args, **kwargs):
        for form in self.deleted_forms:
            try:
                abgabe = Abgabe.objects.get(klausur=form.klausur,
                                            schueler=form.cleaned_data["schueler"])
                abgabe.delete()
            except:
                pass
        for form in self.forms:
            if not form in self.deleted_forms and form.is_valid():
                form.save()

AufgabenFormSet = forms.formset_factory(AufgabenForm, formset=AbgabenFormSet, can_delete=True)
