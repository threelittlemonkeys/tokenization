import sys
import math
from utils import *
from parameters import *

def load_model():
    model = dict()
    fo = open(sys.argv[1])
    for line in fo:
        line = line.strip()
        *w, hL, hR = line.split(" ")
        w = tuple(w)
        hL = float(hL)
        hR = float(hR)
        model[w] = (hL, hR)
    fo.close()
    return model

def load_stopwords():
    stopwords = {("<EOS>",): True}
    fo = open(sys.argv[2])
    for line in fo:
        line = line.strip()
        line = line.lower()
        w = tuple(line.split(" "))
        stopwords[w] = True
    fo.close()
    return stopwords

def decode(scores, tokens_raw, sep):
    i = 0
    output = []
    while i < len(scores):
        score = [x for x in scores[i] if x[1] > 1]
        if not score:
            output.append(tokens_raw[i])
            i += 1
            continue
        score.append((0, 0, 0, 0)) # EOS token
        for k in range(1, len(score)):
            if score[k][3] < score[k - 1][3]: # right word boundary
                j = score[k - 1][1]
                output.append(sep.join(tokens_raw[i:i + j]))
                i += j
                break
    return output

def tokenize(model, stopwords):
    output = []
    stw_len = max(map(len, stopwords)) # maximum stopword length

    # separator
    if LANG in ("ja", "ko", "zh"): sep = ""
    elif LANG == "vi": sep = "_"
    else: sep = " "

    fo = open(sys.argv[3])
    for line in fo:
        line_raw = line.strip()
        line_norm = normalize(line, False)
        if LANG == "vi":
            line_norm = re.sub("_", "__", line)
        tokens_raw = line_norm.split(" ") + ["<EOS>"]
        tokens_norm = line_norm.lower().split(" ") + ["<EOS>"]

        scores = [[] for _ in tokens_raw]
        for i, w in ngram_iter(tokens_norm, NGRAM_SIZES):
            w = tuple(w)
            if w in model:
                scores[i].append((i, len(w), *model[w]))
                if DEBUG:
                    print("score[%d] = " % i, (*model[w], sep.join(w)))

        i, k = 0, 0
        _output = []
        while i < len(tokens_raw):
            f = 0
            for j in range(min(stw_len, len(tokens_raw) - i), 0, -1):
                w = tuple(tokens_norm[i:i + j])
                if w in stopwords:
                    _output.extend(decode(scores[k:i], tokens_raw[k:i], sep))
                    _output.append(sep.join(w))
                    f = k = i = i + j
                    break
            i += not f

        _output = " ".join(_output[:-1])
        output.append(_output)

        if DEBUG:
            print()
            print("line =", line_raw)
            print("tokens =", tokens_raw[:-1])
            print("output =", _output)
            print()

    fo.close()
    return output

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: %s model stopwords test_data" % sys.argv[0])
    model = load_model()
    stopwords = load_stopwords()
    output = tokenize(model, stopwords)
    for line in output:
        print(line)
