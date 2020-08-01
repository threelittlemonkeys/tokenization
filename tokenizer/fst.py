import sys
import re

class _match():
    def __init__(self):
        self.str = ""
        self.span = [0, 0]
        self.state = None

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
            b, a, i = line.split("\t")
            a = set(None if e == "0" else e for e in a.split(","))
            self.fst[i] = (a, b)
            if len(i) > self.maxlen:
                self.maxlen = len(i)
        fo.close()

    def search(self, line):
        i = 0
        matches = [_match()]
        while i < len(line):
            for j in range(self.maxlen, 0, -1):
                j += i
                if j > len(line):
                    continue
                w = line[i:j]
                if w not in self.fst:
                    continue
                if matches[-1].state not in self.fst[w][0]:
                    continue
                if matches[-1].state == None:
                    matches[-1].span[0] = i
                i = j
                matches[-1].str += w
                matches[-1].span[1] = j
                matches[-1].state = self.fst[w][1]
                break
            else:
                if matches[-1].state != None:
                    matches.append(_match())
                    continue
                i += 1
        if matches[-1].state == None:
            matches.pop()
        return matches

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: %s fst text" % sys.argv[0])
    fst = fst(sys.argv[1])
    fo = open(sys.argv[2])
    for line in fo:
        line = line.strip()
        matches = fst.search(line)
        if not matches:
            continue
        print(line)
        for match in matches:
            print(match.str, match.state)
        break
    fo.close()
