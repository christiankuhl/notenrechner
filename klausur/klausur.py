from singleton_decorator import singleton
from numpy import mean
from collections import OrderedDict
import matplotlib.pyplot as plt

RANGES = [[0, .19], [.20, .26], [.27, .33],[.34, .40], [.41, .45],
          [.46, .50], [.51, .55],[.56, .60], [.61, .65], [.66, .70],
          [.71, .75],[.76, .80], [.81, .85], [.86, .90], [.91, .95],
          [.96, float("inf")]]

@singleton
class Klausur(dict):
    def __init__(self, output, input, *args, **kwargs):
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
        self.aufg_avg = [mean([a.points[i]/self.max_points[i] for a in self.values()]) for i in self.max_points]
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
