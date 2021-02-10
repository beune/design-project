from fuzzywuzzy import fuzz
from math import ceil, floor

def combine(first, second, split=" "):
    len_first = len(first)
    len_second = len(second)
    for index in range(max(0, len_first - len_second), len_first - 1):
        if all(map(lambda x, y: x == y, first[index:], second)):
            return first[:index] + second
    return first + split + second


def combine_word(first, second, split=" "):
    # print("first: {}, second: {}".format(first, second))
    split_first = first.lower().split()
    split_second = second.lower().split()
    len_first = len(split_first)
    len_second = len(split_second)
    (key, top) = (None, 65)
    for index in range(max(0, len_first - len_second), len_first):
        scores = [fuzz.ratio(f, s) for f, s in zip(split_first[index:], split_second)]
        score = sum(scores)/len(scores)
        if score > top:
            key = index
            top = score
        # print("score for {}: {} ".format(index, score))
    if key is not None:
        d = (len_first - key) / 2
        # print(d)
        return " ".join(split_first[:-ceil(d)]) + split + " ".join(split_second[floor(d):])
    return first + split + second


if __name__ == "__main__":
    x = combine_word("eens kijken of deze", "eens kijken of deze nieuwe resultaten liggen onze fantastisch")
    print(x)
    y = combine_word("de primaire oorzaak van koude dystrofie herkende verzadiging van", "herken de verzadiging van bloed calcium hypocalcemie etiologie")
    print(y)
