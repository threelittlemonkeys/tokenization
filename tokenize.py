import sys
import math
from utils import *
from parameters import *

def tokenize():
    pass

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: %s model test_data" % sys.argv[0])
    train()
