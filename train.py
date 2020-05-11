import os
import sys
import math
from utils import *
from parameters import *
from collections import defaultdict

def entropy(p):
    return -p * math.log(p)

def train():
    num_data = 0
    freq = defaultdict(lambda: [defaultdict(int), defaultdict(int)])
    model = dict()
    ngram_sizes = [z + 2 for z in NGRAM_SIZES] # append SOS and EOS tokens

    fo = open(sys.argv[1])
    for line in fo:
        line = normalize(line)
        tokens = ("SOS", *line.split(" "), "EOS")
        for _, ngram in ngram_iter(tokens, ngram_sizes):
            wL, *w, wR = ngram
            if not valid(w):
                continue
            w = tuple(w)
            if valid(wL):
                freq[w][0][wL] += 1 # left branching entropy
            if valid(wR):
                freq[w][1][wR] += 1 # right branching entropy
        num_data += 1
        if num_data % 100000 == 0:
            print("%d lines" % num_data)
    fo.close()

    for w, (fL, fR) in freq.items():
        cL = sum(fL.values())
        hL = sum(entropy(f / cL) for f in fL.values())
        cR = sum(fR.values())
        hR = sum(entropy(f / cR) for f in fR.values())
        h = hL * hR
        if h < THRESHOLD:
            continue
        model[w] = h

    return model, num_data

def save_model(model, num_data):
    fo = open("%s/model.%dk" % (os.path.dirname(sys.argv[1]), num_data // 1000), "w")
    for w, h in sorted(model.items(), key = lambda x: -x[1]):
        w = " ".join(w)
        fo.write("%.6f %s\n" % (h, w))
    fo.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s training_data" % sys.argv[0])
    model, num_data = train()
    save_model(model, num_data)
