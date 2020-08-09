import sys
import re

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s fst" % sys.argv[0])
    fo = open(sys.argv[1])
    blocks = fo.read().strip().split("\n\n")
    fo.close()

    for idx, block in enumerate(blocks, 1):
        block = [line.split(" ") for line in block.split("\n")]
        for line in sorted(block, key = lambda x: x[-1]):
            print(" ".join(line))
        if idx < len(blocks):
            print()
