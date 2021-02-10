from fuzzywuzzy import fuzz
from math import ceil, floor

def combine(first, second, split=" "):
    len_first = len(first)
    len_second = len(second)
    for index in range(max(0, len_first - len_second), len_first):
        if all(map(lambda x, y: x == y, first[index:], second)):
            return first[:index] + second
    return first + split + second

