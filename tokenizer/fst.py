import sys
import re

class fst():
    def __init__(self, filename):
        self.fst = dict()
        self.maxlen = 0
        self.read(filename)

    def read(self, filename):
        fo = open(filename)
        for line in fo:
            if line == "\n":
                continue
            line = line[:-1]
            assert re.search("^\S+\t\S+\t\S+$", line)
            a, b, i = line.split("\t")
            a = set(None if e == "0" else e for e in a.split(","))
            self.fst[i] = (a, b)
            if len(i) > self.maxlen:
                self.maxlen = len(i)
        fo.close()

    def search(self, line):
        i = 0
        span = [[]]
        state = [None]
        while i < len(line):
            for j in range(min(len(line), i + self.maxlen), i, -1):
                w = line[i:j]
                if w in self.fst and state[-1] in self.fst[w][0]:
                    if state[-1] == None:
                        span[-1] = [i, 0]
                    i = j
                    span[-1][1] = i
                    state[-1] = self.fst[w][1]
                    break
            else:
                if state[-1] != None:
                    span.append([])
                    state.append(None)
                i += 1
        if state[-1] == None:
            span.pop()
            state.pop()
        return span, state

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: %s fst text" % sys.argv[0])
    fst = fst(sys.argv[1])
    fo = open(sys.argv[2])
    for line in fo:
        line = line.strip()
        span, state = fst.search(line)
        print(line)
        print(span)
        print(state)
        break
    fo.close()
