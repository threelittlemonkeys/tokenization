import sys
import re

fo = open(sys.argv[1])
data = fo.read()[:-1].split("\n")
fo.close()

ln = 1
data_x = data[0::2]
data_y = data[1::2]

for line_x, line_y in zip(data_x, data_y):
    tokens_x = re.split("[\t ]", line_x)
    tokens_y = re.split("[\t ]", line_y)
    assert len(tokens_x) == len(tokens_y)
    output_x = []
    output_y = []
    for x, y in zip(tokens_x, tokens_y):
        if x == "":
            break
        assert y in ("B", "I", "")
        output_x.append(x)
        output_y.append("B" if y == "" else y)
    # print(" ".join(output_x))
    # print(" ".join(output_y))
    print(" ".join("%s/%s" % (x, y) for x, y in zip(output_x, output_y)))
    ln += 1
