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

def tokenize(model):
    output = []

    # separator
    if LANG in ("ja", "ko", "zh"): sep = ""
    elif LANG == "vi": sep = "_"
    else: sep = " "

    fo = open(sys.argv[2])
    for line in fo:
        line = normalize(line, False)
        if LANG == "vi":
            line = re.sub("_", "__", line)
        tkns_raw = line.split(" ")
        tkns_norm = line.lower().split(" ")
        if DEBUG:
            print(line)
            print()

        scores = [[] for _ in tkns_raw]
        for i, w in ngram_iter(tkns_norm, NGRAM_SIZES):
            w = tuple(w)
            if w in model:
                scores[i].append((model[w], len(w)))

        i = 0
        _output = []
        while i < len(scores):
            if not scores[i]:
                _output.append(tkns_raw[i])
                i += 1
                continue
            _scores = scores[i] + [(0, 0)] # append EOS token
            if DEBUG and len(_scores) > 1:
                print("scores[%d] = " % i)
                for h, j in _scores[:-1]:
                    print((" ".join(tkns_raw[i:i + j]), h))
            for j in range(1, len(_scores)):
                if _scores[j] < _scores[j - 1]: # word boundary
                    _output.append(sep.join(tkns_raw[i:i + j]))
                    i += j
                    break
            if DEBUG:
                print()
        _output = " ".join(_output)
        if DEBUG:
            print(_output)
            print()
        output.append(_output)

    fo.close()
    return output

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: %s model test_data" % sys.argv[0])
    model = load_model()
    for line in tokenize(model):
        print(line)
