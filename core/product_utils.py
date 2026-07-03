DEFAULT_PRODUCT = {
    "title": "",
    "platform": "",
    "price": 0.0,
    "reviews": 0,
    "rating": 0,
    "listing_id": "",
    "product_url": "",
    "image_url": "",
    "shop_name": "",
    "shop_url": "",
    "currency": "",
}


def product_to_dict(product):
    if isinstance(product, dict):
        clean_product = DEFAULT_PRODUCT.copy()
        clean_product.update(product)
        return clean_product

    clean_product = DEFAULT_PRODUCT.copy()
    field_names = list(DEFAULT_PRODUCT.keys())

    for index, value in enumerate(product):
        if index >= len(field_names):
            break

        clean_product[field_names[index]] = value

    return clean_product
