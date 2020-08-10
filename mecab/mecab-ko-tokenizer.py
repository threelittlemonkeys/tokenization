import sys
import re

def merge(word, tag, _word, _tag):
    _word = _word.split(" ")
    _tag = _tag.split(" ")
    _len = max(len(_word), len(_tag))
    i = 0
    while i < len(word):
        f = True
        j = i + _len
        if j > len(word):
            break
        for a, b in zip(word[i:j], _word):
            if b == "*":
                continue
            if a[:len(b)] != b:
                f = False
                break
        for a, b in zip(tag[i:j], _tag):
            if b == "*":
                continue
            if a[:len(b)] != b:
                f = False
                break
        if f:
            word[i:j] = ["".join(word[i:j])]
            tag[i:j] = ["+".join(tag[i:j])]
        i += 1

def tokenize(filename):
    fo = open(filename)
    for line in fo:
        line = line.strip().split(" ")
        word, tag = zip(*[re.split("/(?=[^/]+$)", w) for w in line])
        word, tag = list(word), list(tag)
        word0 = " ".join(word)
        tag0 = " ".join(tag)

        merge(word, tag, "", "E E")
        merge(word, tag, "", "J J")
        merge(word, tag, "", "NNB J")
        merge(word, tag, "", "VC E")
        merge(word, tag, "", "VX E")
        merge(word, tag, "", "X E")

        merge(word, tag, "같 *", "V E")
        merge(word, tag, "됐 *", "V E")
        merge(word, tag, "되 *", "V E")
        merge(word, tag, "없 *", "V E")
        merge(word, tag, "있 *", "V E")
        merge(word, tag, "하 *", "V E")
        merge(word, tag, "했 *", "V E")

        word1 = " ".join(word)
        tag1 = " ".join(tag)
        print(word1)
    fo.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s text" % sys.argv[0])
    tokenize(sys.argv[1])
