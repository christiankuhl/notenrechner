import matplotlib.pyplot as plt
import markdown
import os
import webbrowser
from . import IODevice
import numpy as np

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
        plt.savefig("out.png", format='png')
    @staticmethod
    def output(klausur):
        ergebnis = "\n".join([" | ".join(map(str, [n, k.punkte, k.note])) for (n, k) in klausur.items()])
        bar = ":" + "---:|:" * 15 + "---:"
        werte = " | ".join(map(str, klausur.notenspiegel.values()))
        noten = " | ".join(map(str, range(16)))
        kriterien = "\n".join([" | ".join(map(str, [n, l, h])) for (n, [l, h]) in klausur.criteria().items()])
        aufg_avg = "Aufgabe | {}".format(" | ".join(str(n) for n in klausur.max_points))
        aufg_avg += "\n:" + "---:|:" * len(klausur.max_points) + "---:"
        aufg_avg += "\nDurchschn. Punktzahl | {}".format(" | ".join("{:.0f}%".format(100*p) for p in klausur.aufg_avg))
        text = """
# Ergebnisse

## Notendurchschnitt: {4}

## Notenspiegel
{0}
{2}
{3}

![Notenspiegel](out.png)

## Durchschnitt pro Aufgabe
{5}

# Kriterien
Note   |   Von   |   Bis
:-----:|--------:|---------:
{1}""".format(noten, kriterien, bar, werte, klausur.average, aufg_avg)
        result = markdown.markdown(text, extensions=['markdown.extensions.tables'],
                                                        output_format='html5')
        if klausur.admissible():
            admissible = "zulässig"
        else:
            admissible = "unzulässig"
        text = """
# Details
Der Durchschnitt ist {0:.2f} und die Klausur ist {1}.

## Ergebnisse
Klausur   |   Punkte   |   Note
:--------:|-----------:|---------:
{2}

        """.format(klausur.average, admissible, ergebnis)
        if not klausur.admissible():
            boese = "\n\n".join(["Klausur Nr. {0}: {1} Punkte, Note: {2}".format(n, k.punkte, k.note) for n, k in klausur.items()])
            besteboese = """
## Die besten Bösen sind:
{}
    """.format(boese)
            text += besteboese
        detail = markdown.markdown(text, extensions=['markdown.extensions.tables'],
                                                        output_format='html5')
        with open("out.html", "w") as file_handle:
            file_handle.write(result)
        with open("detail.html", "w") as file_handle:
            file_handle.write(detail)
        webbrowser.open_new("out.html")
        webbrowser.open("detail.html")
