import sys
import re
from collections import defaultdict

class bpe():
    def __init__(self, num_iters = 0):
        self.num_iters = num_iters
        self.vocab = []
        self.verbose = True

    @staticmethod
    def tokenize(x):
        x = re.sub("\s+", " ", x)
        x = re.sub("^ | $", "", x)
        x = x.lower()
        x = [[c.replace("_", "__") for c in w] for w in x.split(" ")]
        x = [["_" + w[0], *w[1:]] for w in x]
        return x

    @staticmethod
    def merge(word, pair):
        i = 0
        _word = []
        while i < len(word):
            if i < len(word) - 1 and pair == tuple(word[i:i + 2]):
                _word.append("".join(pair))
                i += 2
                continue
            _word.append(word[i])
            i += 1
        return _word

    def load_data(self, filename):
        data = defaultdict(int)
        fo = open(filename)
        for line in fo:
            line = self.tokenize(line)
            for w in line:
                data[tuple(w)] += 1
        fo.close()
        return data

    def load_vocab(self, filename):
        fo = open(filename)
        for line in fo:
            line = line.strip()
            *w, f = line.split()
            self.vocab.append((tuple(w), f))
        fo.close()

    def save_vocab(self, filename):
        fo = open(filename, "w")
        for w, f in self.vocab:
            print(" ".join(w), f, file = fo)
        fo.close()


    def find_pair(self, data):
        pairs = defaultdict(int)
        for w, f in data.items():
            for i in range(len(w) - 1):
                pairs[w[i], w[i + 1]] += f
        if len(pairs) == 0:
            return None
        return sorted(pairs.items(), key = lambda x: -x[1])[0]

    def merge_data(self, data, pair):
        _data = {}
        for w0, f in data.items():
            w1 = self.merge(w0, pair)
            _data[tuple(w1)] = f
        return _data

    def train(self, filename):
        data = self.load_data(filename)
        for i in range(self.num_iters):
            pair = self.find_pair(data)
            if not pair:
                break
            self.vocab.append(pair)
            data = self.merge_data(data, pair[0])
            w, f = pair
            if self.verbose:
                print("pair[%d] = %s, %d " % (i + 1, w, f))

    def predict(self, line):
        line = self.tokenize(line)
        for pair, _ in self.vocab:
            for i, w0 in enumerate(line):
                w1 = self.merge(w0, pair)
                line[i] = w1
        return " ".join(" ".join(w) for w in line)

if __name__ == "__main__":
    if len(sys.argv) not in (4, 5):
        sys.exit("Usage: %s train|predict vocab data num_iters" % sys.argv[0])

    if sys.argv[1] == "train":
        bpe = bpe(int(sys.argv[4]))
        bpe.train(sys.argv[3])
        bpe.save_vocab(sys.argv[2])

    if sys.argv[1] == "predict":
        bpe = bpe()
        bpe.load_vocab(sys.argv[2])
        fo = open(sys.argv[3])
        for line in fo:
            line = line.strip()
            print(bpe.predict(line))
        fo.close()
