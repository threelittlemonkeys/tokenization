import sys
import math
from utils import *
from parameters import *

def load_model():
    model = dict()
    fo = open(sys.argv[1])
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

def load_stopwords():
    stopwords = dict()
    fo = open(sys.argv[2])
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
    output_pos = [0]
    output_pos.append(0)
    log()
    for i in range(1, len(_scores) - 1):
        wL, w, wR = _scores[i - 1:i + 2]
        if w[1] in (0, 9999):
            output_pos.append(i - 1)
            log("pos[%d] : %s" % (i - 1, "stopword"))
        if wL[1] < w[1] > wR[1]:
            output_pos.append(i - 1)
            log("pos[%d] : left BE" % (i - 1))
        if wL[2] < w[2] > wR[2]:
            output_pos.append(i + w[3] - 1)
            log("pos[%d] : right BE" % (i + w[3] - 1))
    output_pos.append(len(scores))
    output_pos = sorted(set(output_pos))
    output_pos = list(zip(output_pos[:-1], output_pos[1:]))
    output_iob = []
    for i, j in output_pos:
        output_iob.extend("I" if x else "B" for x in range(j - i))
    return output_pos, output_iob

def tokenize(model, stopwords):
    output = []

    # token-in-word separator
    if LANG in ("ja", "ko", "zh"): sep = ""
    elif LANG == "vi": sep = "_"
    else: sep = " "

    fo = open(sys.argv[3])
    for line in fo:
        line = line.strip()
        log("line = %s\n" % line)
        line = normalize(line, False)
        if LANG == "vi":
            line = re.sub("_", "__", line)

        k = [0, 0] # stopword position
        tokens = line.lower().split(" ")
        scores = [0] * len(tokens)
        for i in range(len(tokens)):
            _scores = []
            for j in NGRAM_SIZES:
                if i + j > len(tokens):
                    break
                w = tuple(tokens[i:i + j])
                if w in stopwords and (i == k[0] or i >= k[1]):
                    _scores.append((9999, 9999, 9999, len(w)))
                    k = [i, len(w)]
                elif len(w) > 1 and w in model:
                    _scores.append((*model[w], len(w)))
            if not _scores:
                _scores.append((0, 0, 0, 1))
            scores[i] = max(_scores, key = lambda x: (sum(x[1:3]), x[3]))
            w = sep.join(tokens[i:i + scores[i][3]])
            log("score[%d] =" % i, (*scores[i][:3], w))

        tokens = line.split(" ")
        output_pos, output_iob = decode(scores)
        output_str = " ".join(sep.join(tokens[i:j]) for i, j in output_pos)
        output.append((tokens, output_iob, output_str))
        log("\ntokens =", tokens)
        log("output_iob =", output_iob)
        log("output_str = %s\n" % output_str)

    fo.close()
    return output

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: %s model stopwords test_data" % sys.argv[0])
    model = load_model()
    stopwords = load_stopwords()
    output = tokenize(model, stopwords)
    for tokens, output_iob, output_str in output:
        # string
        # print(output_str)
        # IOB format
        print("\t".join(tokens))
        print("\t".join(output_iob))
