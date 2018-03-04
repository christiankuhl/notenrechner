import matplotlib.pyplot as plt
import markdown
import os
import webbrowser
from . import IODevice
import numpy as np
from flask import Flask, render_template,request
from collections import defaultdict
from klausur import Klausur, KlausurAbgabe
from .templates import OVERVIEW, DETAILS

class HTML(IODevice):
    @staticmethod
    def init():
        return {1: 0, 2: 0, 3: 0}
    app = Flask("Notenrechner")
    @staticmethod
    def init_handler():
        if not os.path.exists(".temp"):
            os.mkdir(".temp")
        HTML.app.run()
    @staticmethod
    def exit_handler():
        os.remove(".temp/figure.png")
        os.rmdir(".temp")
    @staticmethod
    def handle_figure(klausur):
        plt.savefig(".temp/figure.png", format='png')
        plt.savefig("out.png", format='png')
    @staticmethod
    @app.route("/")
    def input():
        return render_template("input.html")
    @staticmethod
    def reshape(request):
        abgaben = defaultdict(defaultdict)
        for key, value in request.form.items():
            abgaben[int(key[:key.find("/")])][int(key[key.find("/")+1:])] = float(value[0])
        Klausur().max_points = abgaben.pop(0)
        Klausur().total = sum(Klausur().max_points)
        for key, value in abgaben.items():
            Klausur()[key] = KlausurAbgabe(value)
        Klausur().calculate()
        return Klausur()
    @staticmethod
    @app.route("/evaluate", methods=["POST"])
    def output(klausur=None, silent=False):
        if not klausur:
            klausur = HTML.reshape(request)
        ergebnis = "\n".join([" | ".join(map(str, [n, k.punkte, k.note])) for (n, k) in klausur.items()])
        bar = ":" + "---:|:" * 15 + "---:"
        werte = " | ".join(map(str, klausur.notenspiegel.values()))
        noten = " | ".join(map(str, range(16)))
        kriterien = "\n".join([" | ".join(map(str, [n, l, h])) for (n, [l, h]) in klausur.criteria().items()])
        aufg_avg = "Aufgabe | {}".format(" | ".join(str(n) for n in klausur.max_points))
        aufg_avg += "\n:" + "---:|:" * len(klausur.max_points) + "---:"
        aufg_avg += "\nDurchschn. Punktzahl | {}".format(" | ".join("{:.0f}%".format(100*p) for p in klausur.aufg_avg))
        text = OVERVIEW.format(noten, kriterien, bar, werte, klausur.average, aufg_avg)
        result = markdown.markdown(text, extensions=['markdown.extensions.tables'],
                                                        output_format='html5')
        if klausur.admissible():
            admissible = "zulässig"
        else:
            admissible = "unzulässig"
        text = DETAILS.format(klausur.average, admissible, ergebnis)
        if not klausur.admissible():
            boese = "\n\n".join(["Klausur Nr. {0}: {1} Punkte, Note: {2}".format(n, k.punkte, k.note) for n, k in klausur.items()])
            besteboese = """
## Die besten Bösen sind:
{}
    """.format(boese)
            text += besteboese
        detail = markdown.markdown(text, extensions=['markdown.extensions.tables'],
                                                        output_format='html5')
        return detail
        # with open("out.html", "w") as file_handle:
        #     file_handle.write(result)
        # with open("detail.html", "w") as file_handle:
        #     file_handle.write(detail)
        # if not silent:
        #     webbrowser.open_new("out.html")
        #     webbrowser.open("detail.html")
