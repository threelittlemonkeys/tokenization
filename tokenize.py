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

def decode(scores, tokens):
    output = [0]
    for i in range(1, len(scores)):
        dL = scores[i][0] - scores[i - 1][0]
        dR = scores[i][1] - scores[i - 1][1]
        if dL >= 0: # left word boundary
            output.append(i)
        if dR >= 0: # left word boundary
            output.append(i + scores[i][2])
    output.append(len(scores))

    # TODO
    output = list(set(output))

    output = [tokens[i:j] for i, j in zip(output[:-1], output[1:])]
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
        line = line.strip()
        _line = normalize(line, False)
        if LANG == "vi":
            _line = re.sub("_", "__", line)
        tokens = _line.split(" ") + ["<EOS>"]
        _tokens = _line.lower().split(" ") + ["<EOS>"]

        scores = [0] * len(tokens)
        for i in range(len(tokens)):
            _scores = []
            for j in NGRAM_SIZES:
                if i + j > len(tokens):
                    break
                w = tuple(_tokens[i:i + j])
                if w in model:
                    _scores.append((*model[w], len(w)))
            if not _scores:
                _scores.append((0, 0, 1))
            scores[i] = max(_scores, key = lambda x: sum(x[:2]))
            if DEBUG:
                w = sep.join(tokens[i:i + scores[i][2]])
                print("score[%d] = " % i, (*scores[i][:2], w))

        i, k = 0, 0
        _output = []
        while i < len(tokens):
            f = 0
            for j in range(min(stw_len, len(tokens) - i), 0, -1):
                w = tuple(_tokens[i:i + j])
                if w in stopwords:
                    _output.extend(decode(scores[k:i], tokens[k:i]))
                    _output.append(w)
                    f = k = i = i + j
                    break
            i += not f

        _output = " ".join(sep.join(w) for w in _output[:-1])
        output.append(_output)

        if DEBUG:
            print("\nline = %s" % line)
            print("output = %s\n" % _output)
            input()

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
