from klausur.constants import RANGES

def note(percentage):
    return [n for (n, [l,h]) in enumerate(RANGES) if l <= percentage and h >= percentage][0]
