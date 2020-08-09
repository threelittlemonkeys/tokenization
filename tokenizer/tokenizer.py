import sys
import re
import time
from fst import fst as _fst

from tokenizer_en import tokenize_en
from tokenizer_ko import tokenize_ko

RE_SPACE = re.compile("[\s\u3000]+") # whitespace
RE_NON_ALNUM = re.compile("([^ a-z0-9\u4E00-\u9FFF\uAC00-\uD7AF])", re.I) # non-alphanumeric

def sizeof(x, ids = set()):
    z = sys.getsizeof(x)
    _id = id(x)
    if _id in ids:
        return 0
    ids.add(_id)
    if isinstance(x, dict):
        z += sum(sizeof(k, ids) for k in x.keys())
        z += sum(sizeof(v, ids) for v in x.values())
    elif hasattr(x, '__dict__'):
        z += sizeof(x.__dict__, ids)
    elif hasattr(x, '__iter__') and not isinstance(x, (str, bytes, bytearray)):
        z += sum(sizeof(i, ids) for i in x)
    return z

def normalize(line):
    line = RE_NON_ALNUM.sub(" \\1 ", line)
    line = RE_SPACE.sub(" ", line)
    line = line.strip()
    return line

def tokenize(lang, filename):

    fst = _fst()
    timer = time.time()
    if lang == "ko":
        fst.read("tokenizer_ko.ADP.fst")
        fst.read("tokenizer_ko.VB.fst")
        # fst.read("tokenizer_ko.EC.fst")
        # fst.read("tokenizer_ko.EF.fst")
        # fst.read("tokenizer_ko.ET.fst")
        # fst.read("tokenizer_ko.J.fst")
    timer = time.time() - timer
    fst_size = sizeof(fst.fst) / 1024
    sys.stderr.write("FSTs loaded (%f KB, %f seconds)\n" % (fst_size, timer))

    timer = time.time()
    with open(filename) as fo:
        for idx, line in enumerate(fo, 1):
            line = normalize(line)
            line = tokenize_en(line)
            if lang == "ko":
                line = tokenize_ko(fst, line)
            print(line)
    timer = time.time() - timer
    sys.stderr.write("%d lines\n" % idx)
    sys.stderr.write("%f seconds\n" % timer)
    sys.stderr.write("%f lines per second\n" % (idx / timer))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: %s lang text" % sys.argv[0])
    tokenize(*sys.argv[1:])
