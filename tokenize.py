import sys
import re
import math

NGRAM_SIZES = (1, 2, 3)
THRESHOLD = 1.38 # Vietnamese
RE_NON_ALNUM = re.compile("([,.?!:;@#$%^&*()_+='\"-]+)")

def normalize(x):
    x = RE_NON_ALNUM.sub(r" \1 ", x)
    x = re.sub("\s+", " ", x)
    x = x.strip()
    x = x.lower()
    return x

def ngram_iter(x):
    for j in NGRAM_SIZES:
        for i in range(len(x) - j):
            ngram = tuple(x[i:i + j + 1])
            yield ngram

def valid(x):
    for x in x:
        if len(x) == 1:
            return False
        if x.isdigit():
            return False
        if RE_NON_ALNUM.fullmatch(x):
            return False
    return True

def entropy(p):
    return -p * math.log(p)

def branching_entropy():

    cnt = 0
    freq = dict()
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

    be = dict()
    for w0, w1 in freq.items():
        c = sum(w1.values())
        h = sum(entropy(f / c) for f in w1.values())
        be[w0] = h

    return be

def train():
    be = branching_entropy()
    fo = open(sys.argv[1] + ".be", "w")
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
