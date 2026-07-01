from collections import Counter


STOP_WORDS = {
    "the", "and", "for", "with", "a", "an", "of", "to", "in",
    "shirt", "tshirt", "t-shirt"
}


def analyze_keywords(products):
    all_words = []

    for product in products:
        title, platform, price, reviews = product
        words = title.lower().replace("-", " ").split()

        for word in words:
            clean_word = word.strip(".,!?()[]{}")
            if clean_word and clean_word not in STOP_WORDS:
                all_words.append(clean_word)

    return Counter(all_words).most_common(20)