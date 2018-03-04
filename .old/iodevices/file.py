import json
from . import IODevice
from klausur import KlausurAbgabe

class File(IODevice):
    @staticmethod
    def init():
        with open("klausur.out", "r") as file_handle:
            max_points = json.loads(file_handle.readline())
        return max_points

    def input():
        klausuren = []
        with open("klausur.out", "r") as file_handle:
            data = list(file_handle)[1:]
        for row in data:
            row = json.loads(row)
            points_dict = dict(zip(enumerate(row, start=1), row))
            klausuren.append(KlausurAbgabe(points_dict))
        return klausuren


    @staticmethod
    def output(klausur):
        with open("klausur.out", "w") as file_handle:
            file_handle.write(json.dumps(klausur.max_points) + "\n")
            for abgabe in klausur.values():
                file_handle.write(json.dumps(list(abgabe.points.values())) + "\n")

    @staticmethod
    def handle_figure(klausur):
        pass
