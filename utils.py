import re
from parameters import *

'''
0030-0039, 0041-005A, 0061-007A (Basic Latin)
00C0-00FF (Latin-1 Supplement)
0100-017F (Latin Extended-A)
0180-024F (Latin Extended-B)
1E00-1EFF (Latin Extended Additional)
'''

RE_NON_ALNUM = re.compile("([^0-9A-Za-z\u00C0-\u024F\u1E00-\u1EFF]+)")

def normalize(x):
    x = RE_NON_ALNUM.sub(r" \1 ", x)
    x = re.sub("\s+", " ", x)
    x = x.strip()
    x = x.lower()
    return x

def ngram_iter(x):
    for j in NGRAM_SIZES:
        for i in range(len(x) - j):
            ngram = tuple(x[i:i + j + 1])
            yield ngram

def valid(x):
    for x in x:
        if len(x) == 1:
            return False
        if x.isdigit():
            return False
        if RE_NON_ALNUM.fullmatch(x):
            return False
    return True
