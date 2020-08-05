import re

_HANGUL = re.compile("[\uAC00-\uD7AF]")

def tokenize_ko(fst, line):
    tokens = line.split(" ")
    for i, w in enumerate(tokens):
        if not _HANGUL.search(w):
            continue
        for m in fst.finditer(w):
            if not m:
                continue
            p0, p1, st = m
            if not (p0 > 0 and p1 == len(w)):
                continue
            tokens[i] = w[:p0] + " " + w[p0:]
    line = " ".join(tokens)
    return line
