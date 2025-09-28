import re


OVERLOAD = re.compile(r'(устал|выжат|перегруз)', re.I)
PRESSURE = re.compile(r'(давит|срочно|под давлением|горят сроки)', re.I)


def analyze(texts):
    overload = 0
    pressure = 0
    for text in texts:
        if not text:
            continue
        if OVERLOAD.search(text):
            overload += 1
        if PRESSURE.search(text):
            pressure += 1
    return {
        'overload': overload,
        'pressure': pressure,
    }
