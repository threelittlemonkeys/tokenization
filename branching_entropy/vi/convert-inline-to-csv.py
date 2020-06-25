import sys
import re

fo = open(sys.argv[1])
for line in fo:
    line = line.strip()
    line = line.split(" ")
    x, y = zip(*[re.split("/(?=[^/]+$)", x) for x in line])
    assert len(x) == len(y)
    print(" ".join(x))
    print(" ".join(y))
fo.close()
