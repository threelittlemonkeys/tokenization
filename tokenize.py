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
        tokens_cs = line.split(" ")
        tokens_ci = line.lower().split(" ")
        if DEBUG:
            print(line)

        scores = [[] for _ in tokens_ci]
        for i, w in ngram_iter(tokens_ci, NGRAM_SIZES):
            w = tuple(w)
            if w in model:
                scores[i].append((model[w], len(w)))

        i = 0
        _output = []
        while i < len(scores):
            _scores = [x for x in scores[i] if x[1] > 1]
            if _scores:
                _score, _len = max(_scores, key = lambda x: x[1])
                _word = "_".join(tokens_cs[i:i + _len])
                _output.append(_word)
                if DEBUG:
                    for _score, _len  in _scores:
                        _word = "_".join(tokens_ci[i:i + _len])
                        print((i, _word, _score))
                i += _len
            else:
                _output.append(tokens_cs[i])
                i += 1

        output.append(" ".join(_output))
        if DEBUG:
            print()

    fo.close()
    return output

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: %s model test_data" % sys.argv[0])
    model = load_model()
    for line in tokenize(model):
        print(line)
