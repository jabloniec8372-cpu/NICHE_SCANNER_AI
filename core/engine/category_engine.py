from config.categories import PRODUCT_TYPES


def detect_product_type(title):
    title = title.lower()

    for product_type, keywords in PRODUCT_TYPES.items():
        for keyword in keywords:
            if keyword in title:
                return product_type

    return "unknown"