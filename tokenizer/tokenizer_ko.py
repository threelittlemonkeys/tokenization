import re

_HANGUL = re.compile("[\uAC00-\uD7AF]")

def tokenize_ko(line):
    tokens = line.split(" ")
    for i, token in enumerate(tokens):
        if not _HANGUL.search(token):
            continue
    line = " ".join(tokens)
    return line
