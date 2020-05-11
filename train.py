import os
import sys
import math
from utils import *
from parameters import *

def entropy(p):
    return -p * math.log(p)

def branching_entropy():
    cnt = 0
    freq = dict()
    be = dict()

    fo = open(sys.argv[1])
    for line in fo:
        line = normalize(line)
        tokens = line.split(" ")
        for ngram in ngram_iter(tokens):
            if not valid(ngram):
                continue
            *w0, w1 = ngram
            w0 = tuple(w0)
            if w0 not in freq:
                freq[w0] = dict()
            if w1 not in freq[w0]:
                freq[w0][w1] = 0
            freq[w0][w1] += 1
        cnt += 1
        if cnt % 100000 == 0:
            print("%d lines" % cnt)
    fo.close()

    for w0, w1 in freq.items():
        c = sum(w1.values())
        h = sum(entropy(f / c) for f in w1.values())
        be[w0] = h

    return be, cnt

def train():
    be, cnt = branching_entropy()
    fo = open("%s/model.%dk" % (os.path.dirname(sys.argv[1]), cnt // 1000), "w")
    for w, h in sorted(be.items(), key = lambda x: -x[1]):
        if h < THRESHOLD:
            break
        w = " ".join(w)
        fo.write("%.6f %s\n" % (h, w))
    fo.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s training_data" % sys.argv[0])
    train()
