#!/usr/bin/env python3
from singleton_decorator import singleton
from numpy import mean
from collections import OrderedDict

RANGES = [[0, .19], [.20, .26], [.27, .33],[.34, .40], [.41, .45],
          [.46, .50], [.51, .55],[.56, .60], [.61, .65], [.66, .70],
          [.71, .75],[.76, .80], [.81, .85], [.86, .90], [.91, .95],
          [.96, float("inf")]]

class PDF(object):
    @staticmethod
    def output(klausur):
        pass

class Terminal(object):
    @staticmethod
    def init():
        n = int(input("Wie viele Aufgaben gibt es? "))
        max_points = dict()
        for i in range(1, n+1):
            p = float(input("Wie viele Punkte gibt es auf Aufgabe {}? ".format(i)))
            max_points[i] = p
        return max_points

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
    def __init__(self, output=Terminal, input=Terminal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.OutputDevice = output
        self.InputDevice = input
        self.notenspiegel = OrderedDict({n: 0 for n in range(16)})
        self.max_points = self.InputDevice.init()
        self.total = sum(self.max_points.values())

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
    K = Klausur()
    K.input()
    K.calculate()
    K.output()
