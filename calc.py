#!/usr/bin/env python3
from singleton_decorator import singleton
from numpy import mean
from collections import OrderedDict
import matplotlib.pyplot as plt
import os
import markdown
from io import BytesIO
from PIL import Image

RANGES = [[0, .19], [.20, .26], [.27, .33],[.34, .40], [.41, .45],
          [.46, .50], [.51, .55],[.56, .60], [.61, .65], [.66, .70],
          [.71, .75],[.76, .80], [.81, .85], [.86, .90], [.91, .95],
          [.96, float("inf")]]

class IODevice(object):
    @staticmethod
    def init_handler():
        pass
    def exit_handler():
        pass

class HTML(IODevice):
    @staticmethod
    def init_handler():
        if not os.path.exists(".temp"):
            os.mkdir(".temp")
    @staticmethod
    def exit_handler():
        os.remove(".temp/figure.png")
        os.rmdir(".temp")
    @staticmethod
    def handle_figure(klausur):
        plt.savefig(".temp/figure.png", format='png')
    @staticmethod
    def output(klausur):
        ergebnis = "\n".join([" | ".join(map(str, [n, k.punkte, k.note])) for (n, k) in klausur.items()])
        bar = ":" + "---:|:" * 15 + "---:"
        werte = " | ".join(map(str, klausur.notenspiegel.values()))
        noten = " | ".join(map(str, range(16)))
        kriterien = "\n".join([" | ".join(map(str, [n, l, h])) for (n, [l, h]) in klausur.criteria().items()])
        text = """
# Ergebnisse
Klausur   |   Punkte   |   Note
:--------:|-----------:|---------:
{0}

# Notenspiegel
{1}
{3}
{4}

[(.temp/figure.png)]

# Kriterien
Note   |   Von   |   Bis
:-----:|--------:|---------:
{2}""".format(ergebnis, noten, kriterien, bar, werte)
        result = markdown.markdown(text, extensions=['markdown.extensions.tables'],
                                                        output_format='html5')
        with open("out.html", "w") as file_handle:
            file_handle.write(result)
        plt.show()


class PDF(HTML):
    @staticmethod
    def output(klausur):
        pass

class Terminal(IODevice):
    @staticmethod
    def init():
        n = int(input("Wie viele Aufgaben gibt es? "))
        max_points = dict()
        for i in range(1, n+1):
            p = float(input("Wie viele Punkte gibt es auf Aufgabe {}? ".format(i)))
            max_points[i] = p
        return max_points

    @staticmethod
    def handle_figure(klausur):
        klausur.figure = BytesIO()
        plt.savefig(klausur.figure, format='png')

    @staticmethod
    def output(klausur):
        print(klausur)
        print()
        print("Ergebnisse:")
        for n, abgabe in klausur.items():
            print("Klausur {}:".format(n), abgabe)
        if klausur.admissible():
            admissible = "zulässig"
        else:
            admissible = "unzulässig"
        print("Der Schnitt ist {}, und die Klausur ist {}.".format(klausur.average, admissible))
        print()
        if not klausur.admissible():
            print("Die besten Bösen sind:")
            for b in klausur.beste_boese():
                print("Klausur {}:".format(b[0]), b[1])
        print()
        print("Notenspiegel:")
        for note, f in klausur.notenspiegel.items():
            print("{}: {}".format(note, f))
        print()
        print("Kriterien:")
        criteria = klausur.criteria()
        for n, [l, h] in list(criteria.items())[:-1]:
            print("Note {0}: von {1} bis {2} Punkten".format(n, l, h))
        print("Note 15: ab {} Punkten".format(criteria[15][0]))
        plt.show()
        # klausur.figure.seek(0)
        # im = Image.open(klausur.figure)
        # im.show()
        # klausur.figure.close()

    @staticmethod
    def input():
        j = 0
        klausuren = []
        print("Punkte eingeben für die Klausur. {}-mal RETURN drücken zum Berechnen.".format(Klausur().aufgaben()))
        while True:
            j += 1
            points_dict = {}
            print("Klausur Nr.", j)
            for i, _ in enumerate(Klausur().max_points, 1):
                points = input("Aufgabe {}: ".format(i))
                if points:
                    points_dict[i] = float(points)
            if not points_dict:
                break
            abgabe = KlausurAbgabe(points_dict)
            klausuren.append(abgabe)
        return klausuren

@singleton
class Klausur(dict):
    def __init__(self, output=HTML, input=Terminal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.OutputDevice = output
        self.InputDevice = input
        self.notenspiegel = OrderedDict({n: 0 for n in range(16)})
        self.max_points = self.InputDevice.init()
        self.total = sum(self.max_points.values())

    def __enter__(self):
        self.OutputDevice.init_handler()
        return self

    def __exit__(self, *args):
        self.OutputDevice.exit_handler()

    def rh(self, n):
        r = [p/2 for p in range(2*round(self.total) + 1) if self.note(p/2) == n]
        if r:
            return [min(r), max(r)]
        else:
            return ["N/A", "N/A"]

    def criteria(self):
        return OrderedDict({n: self.rh(n) for n in range(16)})

    def number(self):
        return len(self) + 1

    def aufgaben(self):
        return len(self.max_points)

    def note(self, points):
        percentage = round(points/self.total, 2)
        note = [n for (n, [l,h]) in enumerate(RANGES) if l <= percentage and h >= percentage][0]
        self.notenspiegel[note] += 1
        return note

    def calculate(self):
        self.average = mean([a.note for a in self.values()])
        self.create_histogram()

    def output(self):
        self.OutputDevice.output(self)

    def input(self):
        klausuren = self.InputDevice.input()
        for abgabe in klausuren:
            self[self.number()] = abgabe

    def admissible(self):
        return len([a for a in self.values() if a.note < 5]) <= len(self)/2

    def beste_boese(self):
        boese = [a for a in self.items() if a[1].note < 5]
        boese.sort(key=lambda a: a[1].punkte, reverse=True)
        return boese[:round(len(self)/2)-len(boese)]

    def create_histogram(self):
        plt.title("Notenspiegel")
        plt.xlabel("Note")
        plt.ylabel("Frequenz")
        bins = [r - .5 for r in range(17)]
        plt.xticks(range(16))
        plt.hist([a.note for a in self.values()], bins=bins, facecolor='blue', alpha=0.5)
        self.OutputDevice.handle_figure(self)

class KlausurAbgabe(object):
    def __init__(self, punkte):
        self.points = punkte
        self.max_points = Klausur().max_points
        self.total = Klausur().total
        self.punkte = sum(self.points.values())
        self.note = Klausur().note(self.punkte)

    def __repr__(self):
        return "{0} von {1} Punkten, Note: {2}".format(self.punkte, self.total, self.note)


if __name__ == '__main__':
    with Klausur() as K:
        K.input()
        K.calculate()
        K.output()
