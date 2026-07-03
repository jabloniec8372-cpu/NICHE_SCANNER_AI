POD_KEYWORDS = [
    "shirt",
    "t-shirt",
    "tee",
    "hoodie",
    "sweatshirt",
    "pullover",
    "mug",
    "coffee mug",
    "sticker",
    "poster",
    "print",
    "wall art",
    "canvas",
    "tote",
    "bag",
    "phone case",
    "pillow",
    "blanket",
    "svg",
    "png",
    "clipart",
    "sublimation",
    "digital download",
    "pattern",
]

BLOCKED_KEYWORDS = [
    "collar",
    "leash",
    "toy",
    "sculpture",
    "tag",
    "jewelry",
    "keychain",
    "crochet",
    "oil painting",
    "original painting",
    "pet portrait",
]


def is_pod_product(title):
    clean_title = title.lower()

    if any(blocked in clean_title for blocked in BLOCKED_KEYWORDS):
        return False

    return any(keyword in clean_title for keyword in POD_KEYWORDS)