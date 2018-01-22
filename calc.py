#!/usr/bin/env python3
from klausur import Klausur
from iodevices import File, HTML, Terminal

if __name__ == '__main__':
    with Klausur(input=HTML, output=HTML) as K:
        K.input()
        # K.calculate()
        # K.output()
