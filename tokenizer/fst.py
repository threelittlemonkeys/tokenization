import sys
import re

class fst():
    def __init__(self):
        self.fst = dict()
        self.maxlen = 0 # maximum length of input

    def read(self, filename):
        ln = 0
        fo = open(filename)
        for line in fo:
            ln += 1
            if line == "\n":
                continue
            line = line[:-1]
            if not re.search("^\S+ \S+ \S+$", line):
                sys.exit("Error: invalid format on line %d: %s" % (ln, line))
            s1, s0, c = line.split(" ")
            if c not in self.fst:
                self.fst[c] = dict()
            for s0 in s0.split(","):
                if s0 not in self.fst[c]:
                    self.fst[c][s0] = set()
                for s1 in s1.split(","):
                    if s1 in self.fst[c][s0]:
                        sys.exit("Error: duplicate transition on line %d: %s" % (ln, line))
                    self.fst[c][s0].add(s1)
            if len(c) > self.maxlen:
                self.maxlen = len(c)
        fo.close()

    def find(self, line, p0, s0):
        for p1 in range(self.maxlen):
            p1 += p0 + 1
            if p1 > len(line):
                break
            w = line[p0:p1]
            if w not in self.fst:
                continue
            if s0 not in self.fst[w]:
                continue
            for s1 in self.fst[w][s0]:
                for p3, s1 in self.find(line, p1, s1):
                    yield (len(w) + p3, s1)
        yield (0, s0)

    def finditer(self, line):
        for i in range(len(line)):
            j, st = max(self.find(line, i, "0"))
            yield (i, i + j, st) if j else None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: %s fst text" % sys.argv[0])
    fst = fst(sys.argv[1])
    fo = open(sys.argv[2])
    for line in fo:
        line = line.strip()
        print(line)
        for m in fst.finditer(line):
            if not m:
                continue
            i, j, st = m
            print(line[i:j], st)
    fo.close()
