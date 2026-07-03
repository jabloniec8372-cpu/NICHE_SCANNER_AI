from collections import Counter
import re


STOP_WORDS = {
    "the",
    "and",
    "for",
    "with",
    "a",
    "an",
    "of",
    "to",
    "in",
    "on",
    "your",
    "my",
    "our",
    "is",
    "are",
    "this",
    "that",
    "shirt",
    "tshirt",
    "t-shirt",
    "tee",
    "hoodie",
    "sweatshirt",
    "mug",
    "poster",
    "sticker",
    "gift",
    "custom",
    "digital",
    "download",
}


def analyze_keywords(products):
    counter = Counter()

    for product in products:
        title = product[0].lower()

        words = re.findall(r"[a-zA-Z']+", title)

        for word in words:
            if len(word) < 3:
                continue

            if word in STOP_WORDS:
                continue

            counter[word] += 1

    return counter.most_common(20)