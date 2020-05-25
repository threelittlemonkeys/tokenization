import sys
import re

RE_VIETNAMESE_SYLLABLE = re.compile("(b|c|ch|d|đ|g|gh|gi|h|k|kh|l|m|n|ng|ngh|nh|p|ph|q|qu|r|s|t|th|tr|v|x)?[aăâeêioôơuưyàằầèềìòồờùừỳảẳẩẻểỉỏổởủửỷãẵẫẽễĩõỗỡũữỹáắấéếíóốớúứýạặậẹệịọộợụựỵ]{,3}(c|ch|m|n|ng|nh|p|t)?")

for line in sys.stdin:
    tokens = line.strip().split(" ")
    for w in tokens:
        if RE_VIETNAMESE_SYLLABLE.fullmatch(w):
            print(w)
