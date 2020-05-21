import os
import sys
import math
from utils import *
from parameters import *
from collections import defaultdict

def valid(ls):
    for w in ls:
        if w.isnumeric():
            return False
        if RE_NON_ALNUM.fullmatch(w):
            return False
    return True

def entropy(p):
    return -p * math.log(p)

def train():
    vocab = defaultdict(lambda: [0, defaultdict(int), defaultdict(int)])
    model = dict()
    num_data = 0
    ngram_sizes = [z + 2 for z in NGRAM_SIZES] # append SOS and EOS tokens

    printl("calculating token frequencies")
    fo = open(sys.argv[1])
    for line in fo:
        line = normalize(line)
        tokens = ("<SOS>", *line.split(" "), "<EOS>")
        for _, ngram in ngram_iter(tokens, ngram_sizes):
            wL, *w, wR = ngram
            if not valid(w):
                continue
            w = tuple(w)
            vocab[w][0] += 1
            vocab[w][1][wL] += 1
            vocab[w][2][wR] += 1
        num_data += 1
        if num_data % 100000 == 0:
            printl("%d lines, %d tokens" % (num_data, len(vocab)))
    fo.close()

    printl("calculating branching entropies")
    for w, (freq, fL, fR) in vocab.items():
        hL = sum(entropy(f / freq) for f in fL.values()) # left BE
        hR = sum(entropy(f / freq) for f in fR.values()) # right BE
        if hL < THRESHOLD and hR < THRESHOLD:
            continue
        model[w] = (freq, hL, hR)

    return model, num_data

def save_model(model, num_data):
    num_data //= 1000
    filename = "%s/model.%dk" % (os.path.dirname(sys.argv[1]), num_data)
    printl("saving model")
    fo = open(filename, "w")
    for w, (freq, hL, hR) in sorted(model.items(), key = lambda x: -x[1][-1]):
        w = " ".join(w)
        fo.write("%s %d %.6f %.6f\n" % (w, freq, hL, hR))
    fo.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s training_data" % sys.argv[0])
    printl("LANG =", LANG)
    printl("NGRAM_SIZES =", NGRAM_SIZES)
    printl("THRESHOLD =", THRESHOLD)
    model, num_data = train()
    save_model(model, num_data)
