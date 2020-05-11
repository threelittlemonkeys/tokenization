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
    fo = open(sys.argv[2])
    output = []
    for line in fo:
        line = normalize(line, False)
        line = re.sub("_", "__", line)
        tkns_raw = line.split(" ")
        tkns_norm = line.lower().split(" ")
        if DEBUG:
            print(line)

        scores = [[] for _ in tkns_raw]
        for i, w in ngram_iter(tkns_norm, NGRAM_SIZES):
            w = tuple(w)
            if w in model:
                scores[i].append((model[w], len(w)))

        i = 0
        _output = []
        while i < len(scores):
            if not scores[i]:
                i += 1
                continue
            _scores = scores[i] + [(0, 0)]
            if DEBUG and len(_scores) > 1:
                print("scores[%d] = " % i)
                for h, j in _scores[:-1]:
                    print(("_".join(tkns_raw[i:i + j]), h))
            for j in range(1, len(_scores)):
                if _scores[j] < _scores[j - 1]:
                    _output.append("_".join(tkns_raw[i:i + j]))
                    i += j
                    break
            if DEBUG:
                print()
        output.append(" ".join(_output))

    fo.close()
    return output

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: %s model test_data" % sys.argv[0])
    model = load_model()
    for line in tokenize(model):
        print(line)
