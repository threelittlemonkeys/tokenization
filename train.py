import os
import sys
import math
from utils import *
from parameters import *

def entropy(p):
    return -p * math.log(p)

def train():
    num_data = 0
    freq = dict()
    model = dict() # branching entropy
    ngram_sizes = [z + 1 for z in NGRAM_SIZES]

    fo = open(sys.argv[1])
    for line in fo:
        line = normalize(line)
        tokens = line.split(" ")
        for _, ngram in ngram_iter(tokens, ngram_sizes):
            if not valid(ngram):
                continue
            *w0, w1 = ngram
            w0 = tuple(w0)
            if w0 not in freq:
                freq[w0] = dict()
            if w1 not in freq[w0]:
                freq[w0][w1] = 0
            freq[w0][w1] += 1
        num_data += 1
        if num_data % 100000 == 0:
            print("%d lines" % num_data)
    fo.close()

    for w0, w1 in freq.items():
        c = sum(w1.values())
        h = sum(entropy(f / c) for f in w1.values())
        model[w0] = h

    return model, num_data

def save_model(model, num_data):
    fo = open("%s/model.%dk" % (os.path.dirname(sys.argv[1]), num_data // 1000), "w")
    for w, h in sorted(model.items(), key = lambda x: -x[1]):
        if h < THRESHOLD:
            break
        w = " ".join(w)
        fo.write("%.6f %s\n" % (h, w))
    fo.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s training_data" % sys.argv[0])
    model, num_data = train()
    save_model(model, num_data)
