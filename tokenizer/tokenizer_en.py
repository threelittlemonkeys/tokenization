import re

_APOS_R = re.compile(r"\b(goin) '", re.I)
_APOS_L = re.compile(r"' (cause|d|em|ll|m|s|t|re|ve)\b", re.I)
_NOT = re.compile(r"\b(ca|could|did|does|do|had|has|have|is|was|wo|would)n 't\b", re.I)

def tokenize_en(line):
    line = _APOS_L.sub(r"'\1", line)
    line = _APOS_R.sub(r"\1'", line)
    line = _NOT.sub(r"\1n't", line)
    return line
