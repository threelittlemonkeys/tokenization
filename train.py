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
    vocab = defaultdict(lambda: [defaultdict(int), defaultdict(int)])
    model = dict()
    num_data = 0
    ngram_sizes = [z + 2 for z in NGRAM_SIZES] # append EOS tokens

    print("calculating token frequencies")
    fo = open(sys.argv[1])
    for line in fo:
        line = normalize(line)
        tokens = ("<SOS>", *line.split(" "), "<EOS>")
        for _, ngram in ngram_iter(tokens, ngram_sizes):
            wL, *w, wR = ngram
            if not valid(w):
                continue
            w = tuple(w)
            vocab[w][0][wL] += 1
            vocab[w][1][wR] += 1
        num_data += 1
        if num_data % 100000 == 0:
            print("%d lines, %d tokens" % (num_data, len(vocab)))
    fo.close()

    print("calculating entropy")
    for w, (fL, fR) in vocab.items():
        zL = sum(fL.values())
        hL = sum(entropy(f / zL) for f in fL.values())
        zR = sum(fR.values())
        hR = sum(entropy(f / zR) for f in fR.values())
        if hL < THRESHOLD and HR < THRESHOLD:
            continue
        model[w] = (hL, hR)

    print("calculating mutual information")

    return model, num_data

def save_model(model, num_data):
    num_data //= 1000
    filename = "%s/model.%dk" % (os.path.dirname(sys.argv[1]), num_data)
    print("saving model")
    fo = open(filename, "w")
    for w, (hL, hR) in sorted(model.items(), key = lambda x: -x[1][-1]):
        w = " ".join(w)
        fo.write("%s %.6f %.6f %.6f\n" % (w, hL, hR))
    fo.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s training_data" % sys.argv[0])
    print("LANG =", LANG)
    print("NGRAM_SIZES =", NGRAM_SIZES)
    print("THRESHOLD =", THRESHOLD)
    model, num_data = train()
    save_model(model, num_data)
