import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
from . import IODevice
from klausur import KlausurAbgabe, Klausur

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
