import sys
import re
from collections import defaultdict

class bpe():
    def __init__(self, num_iters = 0):
        self.num_iters = num_iters
        self.verbose = True
        pass

    def load_data(self, filename):
        data = defaultdict(int)
        fo = open(filename)
        for line in fo:
            line = self.normalize(line)
            for w in line.split():
                data[tuple(["_" + w[0], *w[1:]])] += 1
        fo.close()
        return data

    def load_model(self, filename):
        subword = []
        fo = open(filename)
        for line in fo:
            line = line.strip()
            line = line.split()
            subword.append((line[0], line[1]))
        fo.close()
        return subword

    def save_model(self, subword, filename):
        fo = open(filename, "w")
        for w, f in subword:
            fo.write("%s %d\n" % ("".join(w), f))
        fo.close()

    def normalize(self, x):
        x = re.sub("\s+", " ", x)
        x = re.sub("^ | $", "", x)
        x = x.lower()
        return x

    def find_pair(self, data):
        pairs = defaultdict(int)
        for w, f in data.items():
            for i in range(len(w) - 1):
                pairs[w[i], w[i + 1]] += f
        if len(pairs) == 0:
            return None
        return sorted(pairs.items(), key = lambda x: -x[1])[0]

    def merge_pair(self, data, pair):
        merged = {}
        for w0, f in data.items():
            i = 0
            w1 = []
            while i < len(w0):
                if i < len(w0) - 1 and pair == (w0[i], w0[i + 1]):
                    w1.append("".join(pair))
                    i += 2
                    continue
                w1.append(w0[i])
                i += 1
            merged[tuple(w1)] = f
        return merged

    def train(self, filename):
        data = self.load_data(filename)
        subword = []
        for i in range(self.num_iters):
            pair = self.find_pair(data)
            if not pair:
                break
            subword.append(pair)
            data = self.merge_pair(data, pair[0])
            if self.verbose:
                print("iteration = %d" % i)
                print("pair =", ("".join(pair[0]), pair[1]))
        if self.verbose:
            print("%d subwords in total" % len(subword))
        return subword

    def predict(self, subword, line):
        line = [["_" + w[0]] + list(w[1:]) for w in line.split()]
        for pair in subword:
            for i in range(len(line)):
                j = 0
                tmp = []
                while j < len(line[i]):
                    if pair == tuple(line[i][j:j + 2]):
                        tmp.append("".join(pair))
                        j += 2
                        continue
                    tmp.append(line[i][j])
                    j += 1
                line[i] = tmp
        return " ".join(" ".join(w)[1:] for w in line)

if __name__ == "__main__":
    if len(sys.argv) not in (4, 5):
        sys.exit("Usage: %s train|predict model data (num_iters)" % sys.argv[0])
    if sys.argv[1] == "train":
        num_iters = len(sys.argv) == 5:

        bpe = bpe(int(sys.argv[4]))
        subword = bpe.train(sys.argv[3])
        bpe.save_model(subword, sys.argv[2])
    if sys.argv[1] == "predict":
        bpe = bpe()
        subword = bpe.load_model(sys.argv[2])
        fo = open(sys.argv[3])
        for line in fo:
            line = line.strip()
            print(bpe.predict(subword, line))
        fo.close()
