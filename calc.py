#!/usr/bin/env python3
from klausur import Klausur
from iodevices import File, HTML

if __name__ == '__main__':
    with Klausur(input=File, output=HTML) as K:
        K.input()
        K.calculate()
        K.output()
