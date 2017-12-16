import matplotlib.pyplot as plt
import markdown
import os
from . import IODevice

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
