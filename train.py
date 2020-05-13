import os
import sys
import math
from utils import *
from parameters import *
from collections import defaultdict

def valid(ls):
    for w in ls:
        if RE_NON_ALNUM.fullmatch(w):
            return False
    return True

def entropy(p):
    return -p * math.log(p)

def train():
    freq = defaultdict(lambda: [defaultdict(int), defaultdict(int)])
    model = dict()
    num_data = 0
    ngram_sizes = [z + 1 for z in NGRAM_SIZES] # append EOS tokens

    print("calculating frequencies")
    fo = open(sys.argv[1])
    for line in fo:
        line = normalize(line)
        tkns = ("<SOS>", *line.split(" "), "<EOS>")
        for _, ngram in ngram_iter(tkns, ngram_sizes):
            wL, *w, wR = ngram
            if not valid(w):
                continue
            w = tuple(w)
            freq[w][0][wL] += 1
            freq[w][1][wR] += 1
        num_data += 1
        if num_data % 100000 == 0:
            print("%d lines" % num_data)
    fo.close()

    print("calculating entropies")
    for w, (fL, fR) in freq.items():
        zL = sum(fL.values())
        hL = sum(entropy(f / zL) for f in fL.values())
        zR = sum(fR.values())
        hR = sum(entropy(f / zR) for f in fR.values())
        model[w] = (hL, hR, hL + hR)

    return model, num_data

def save_model(model, num_data):
    num_data //= 1000
    filename = "%s/model.%dk" % (os.path.dirname(sys.argv[1]), num_data)
    print("saving model")
    fo = open(filename, "w")
    for w, (hL, hR, h) in sorted(model.items(), key = lambda x: -x[1][-1]):
        w = " ".join(w)
        fo.write("%s %.6f %.6f %.6f\n" % (w, hL, hR, h))
    fo.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s training_data" % sys.argv[0])
    print("LANG =", LANG)
    print("NGRAM_SIZES =", NGRAM_SIZES)
    print("THRESHOLD =", THRESHOLD)
    model, num_data = train()
    save_model(model, num_data)
