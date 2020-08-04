import sys
import re

class fst():
    def __init__(self, filename):
        self.fst = dict()
        self.maxlen = 0 # maximum length of input
        self.read(filename)

    def read(self, filename):
        ln = 0
        fo = open(filename)
        for line in fo:
            ln += 1
            if line == "\n":
                continue
            line = line[:-1]
            if not re.search("^\S+\t\S+\t\S+$", line):
                sys.exit("Syntax error on line %d: %s" % (ln, line))
            s1, s0, c = line.split("\t")
            if c not in self.fst:
                self.fst[c] = dict()
            s1 = s1.split(",")
            for s0 in s0.split(","):
                if s0 not in self.fst[c]:
                    self.fst[c][s0] = set()
                self.fst[c][s0].update(s1)
            if len(c) > self.maxlen:
                self.maxlen = len(c)
        fo.close()

    def match(self, line, i, s0):
        for j in range(self.maxlen):
            j += i
            if j > len(line):
                break
            w = line[i:j]
            if w not in self.fst:
                continue
            if s0 not in self.fst[w]:
                continue
            for s1 in self.fst[w][s0]:
                for m in self.match(line, i + len(w), s1):
                    yield (i, w + m[1],  m[2])
        yield (i, "", s0)

    def search(self, line):
        for i in range(len(line)):
            m = list(self.match(line, i, "0"))
            print(m)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: %s fst text" % sys.argv[0])
    fst = fst(sys.argv[1])
    fo = open(sys.argv[2])
    for line in fo:
        line = line.strip()
        print(line)
        fst.search(line)
        break
    fo.close()
