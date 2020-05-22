import sys
import re

fo = open(sys.argv[1])
data = fo.read()[:-1].split("\n")
fo.close()

ln = 1
data_x = data[0::2]
data_y = data[1::2]

for line_x, line_y in zip(data_x, data_y):
    line_x = re.split("[\t ]", line_x)
    line_y = re.split("[\t ]", line_y)
    output_x = []
    output_y = []
    for x, y in zip(line_x, line_y):
        if x == "":
            break
        if y not in ("B", "I", ""):
            sys.exit("Error: wrong tag '%s' at line %d" % (y, ln * 2))
        output_x.append(x)
        output_y.append("B" if y == "" else y)
    # print(" ".join(output_x))
    # print(" ".join(output_y))
    print(" ".join("%s/%s" % (x, y) for x, y in zip(output_x, output_y)))
    ln += 1
