from klausur.constants import RANGES

def note(percentage):
    percentage = round(percentage, 2)
    return [n for (n, [l,h]) in enumerate(RANGES) if l <= percentage and h >= percentage][0]
