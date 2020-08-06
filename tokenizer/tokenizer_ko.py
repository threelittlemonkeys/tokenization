import re

_HANGUL = re.compile("[\uAC00-\uD7AF]")

def tokenize_ko(fst, line):
    tokens = line.split(" ")
    for i, w in enumerate(tokens):
        if not _HANGUL.search(w):
            continue
        m = list(fst.finditer(w))
        m = list(filter(lambda x: x and x[1] == len(w), m))
        if m:
            j = min(m)[0] # longest match
            if j == 0:
                continue
            tokens[i] = w[:j] + " " + w[j:]
    line = " ".join(tokens)
    return line
