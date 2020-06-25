import sys
from utils import *

def load_model(filename):
    model = dict()
    fo = open(filename)
    for line in fo:
        line = line.strip()
        *w, freq, hL, hR = line.split(" ")
        w = tuple(w)
        freq = int(freq)
        hL = float(hL)
        hR = float(hR)
        model[w] = (freq, hL, hR)
    fo.close()
    return model

def load_stopwords(filename):
    stopwords = dict()
    fo = open(filename)
    for line in fo:
        line = line.strip()
        w, f = line.split("\t")
        w = tuple(w.split(" "))
        if f == "True":
            stopwords[w] = True
    fo.close()
    return stopwords

def decode(scores):
    _scores = [(0, 0, 0, 0), *scores, (0, 0, 0, 0)] # append SOS/EOS tokens
    output_pos = set()
    output_pos.add(0)
    printl()
    for i in range(len(scores)):
        wL, w, wR = _scores[i:i + 3]
        if w[1] == 0:
            if i < max(output_pos):
                continue
            output_pos.add(i) # left word boundary
            output_pos.add(i + 1) # right word boundary
            printl("pos[%d] : unknown" % i)
        if w[1] == 9999:
            output_pos.add(i)
            printl("pos[%d] : stopword" % i)
        if wL[1] < w[1] > wR[1]:
            output_pos.add(i)
            printl("pos[%d] : left BE" % i)
        if wL[2] < w[2] > wR[2]:
            output_pos.add(i + w[3])
            printl("pos[%d] : right BE" % (i + w[3]))
    output_pos.add(len(scores))
    output_pos = sorted(output_pos)
    output_pos = list(zip(output_pos[:-1], output_pos[1:]))
    output_iob = []
    for i, j in output_pos:
        output_iob.extend("I" if x else "B" for x in range(j - i))
    return output_pos, output_iob

def tokenize(model, stopwords, filename):
    y1 = []

    # token-in-word separator
    if LANG in ("ja", "ko", "zh"): sep = ""
    elif LANG == "vi": sep = "_"
    else: sep = " "

    fo = open(filename)
    for x0 in fo:
        x0 = x0.strip()
        y0 = tuple()
        if re.match("\S+/[^ /]+( \S+/[^ /]+)*$", x0):
            x0, y0 = zip(*[re.split("/(?=[^/]+$)", x) for x in x0.split(" ")])
            x0 = " ".join(x0)
        x0 = normalize(x0, False).split(" ")
        x1 = [x.lower() for x in x0]
        k = [0, 0] # stopword position
        scores = [0] * len(x1)
        for i in range(len(x1)):
            _scores = []
            for j in NGRAM_SIZES:
                if i + j > len(x1):
                    break
                w = tuple(x1[i:i + j])
                if w in stopwords and (i == k[0] or i >= k[1]):
                    _scores.append((9999, 9999, 9999, len(w)))
                    k = [i, len(w)]
                elif len(w) > 1 and w in model:
                    _scores.append((*model[w], len(w)))
            if not _scores:
                _scores.append((0, 0, 0, 1))
            scores[i] = max(_scores, key = lambda x: (sum(x[1:3]), x[3]))
            w = sep.join(x1[i:i + scores[i][3]])
            printl("score[%d] =" % i, (*scores[i][:3], w))

        y1_pos, y1_iob = decode(scores)
        y1_str = " ".join(sep.join(x0[i:j]) for i, j in y1_pos)
        y1.append((x0, y0, y1_iob, y1_str))

        printl("\ntokens =", x0)
        printl("output_iob =", y1_iob)
        printl("output_str = %s\n" % y1_str)

    fo.close()
    return y1 

if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit("Usage: %s model stopwords format test_data" % sys.argv[0])
    model = load_model(sys.argv[1])
    stopwords = load_stopwords(sys.argv[2])
    output = tokenize(model, stopwords, sys.argv[4])
    for x0, _, y1_iob, y1_str in output:
        if sys.argv[3] == "str":
            print(y1_str)
        if sys.argv[3] == "iob-inline":
            print(" ".join("%s/%s" % (x, y) for x, y in zip (x0, y1_iob)))
        if sys.argv[3] == "iob-csv":
            print(" ".join(x0))
            print(" ".join(y1_iob))
