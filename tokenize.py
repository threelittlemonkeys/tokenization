import sys
import math
from utils import *
from parameters import *

def load_model():
    model = dict()
    fo = open(sys.argv[1])
    for line in fo:
        line = line.strip()
        h, *w = line.split(" ")
        w = tuple(w)
        h = float(h)
        model[w] = h
    fo.close()
    return model

def load_stopwords():
    stopwords = {("<EOS>",): True}
    fo = open(sys.argv[2])
    for line in fo:
        line = line.strip()
        line = line.lower()
        w = tuple(line.split(" "))
        stopwords[w] = True
    fo.close()
    return stopwords

def decode(scores, tkns_raw, sep):
    i = 0
    output = []
    while i < len(scores):
        # _scores = [x for x in scores[i] if x[2] > 1]
        _scores = scores[i][:]
        if not _scores:
            output.append(tkns_raw[i])
            i += 1
            continue
        _scores.append((0, 0, 0)) # EOS token
        if DEBUG and len(_scores) > 1:
            for p, h, j in _scores[:-1]:
                print("scores[%d] = " % p, (" ".join(tkns_raw[i:i + j]), h))
        for k in range(1, len(_scores)):
            if _scores[k] < _scores[k - 1]: # word boundary
                j = _scores[k - 1][2]
                output.append(sep.join(tkns_raw[i:i + j]))
                i += j
                break
    return output

def tokenize(model):
    output = []

    # separator
    if LANG in ("ja", "ko", "zh"): sep = ""
    elif LANG == "vi": sep = "_"
    else: sep = " "

    fo = open(sys.argv[3])
    for line in fo:
        line = normalize(line, False)
        if LANG == "vi":
            line = re.sub("_", "__", line)
        tkns_raw = line.split(" ") + ["<EOS>"]
        tkns_norm = line.lower().split(" ") + ["<EOS>"]

        scores = [[] for _ in tkns_raw]
        for i, w in ngram_iter(tkns_norm, NGRAM_SIZES):
            w = tuple(w)
            if w in model:
                scores[i].append((i, model[w], len(w)))

        i, k = 0, 0
        _output = []
        while i < len(tkns_raw):
            f = 0
            for j in range(max(map(len, stopwords)), 0, -1):
                if i + j > len(tkns_raw):
                    continue
                w = tuple(tkns_norm[i:i + j])
                if w in stopwords:
                    _output.extend(decode(scores[k:i], tkns_raw[k:i], sep))
                    _output.append(sep.join(w))
                    f = k = i = i + j
                    break
            i += not f

        _output = " ".join(_output[:-1])
        output.append(_output)

        if DEBUG:
            print("\n" + line)
            print(_output + "\n")
            input()

    fo.close()
    return output

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: %s model stopwords test_data" % sys.argv[0])
    model = load_model()
    stopwords = load_stopwords()
    output = tokenize(model)
    for line in output:
        print(line)
