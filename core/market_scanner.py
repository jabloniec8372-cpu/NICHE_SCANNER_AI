from connectors.etsy_api import search_etsy_products


def scan_keyword(keyword):
    etsy_products = search_etsy_products(keyword)

    if etsy_products:
        return etsy_products

    products = [
        {
            "title": f"Funny {keyword} Vintage Shirt",
            "platform": "Etsy",
            "price": 19.99,
            "reviews": 842,
        },
        {
            "title": f"Retro {keyword} Hoodie",
            "platform": "Redbubble",
            "price": 34.50,
            "reviews": 620,
        },
        {
            "title": f"Cute {keyword} Coffee Mug",
            "platform": "Amazon Handmade",
            "price": 16.99,
            "reviews": 1200,
        },
        {
            "title": f"Minimalist {keyword} Sticker",
            "platform": "TeePublic",
            "price": 4.99,
            "reviews": 260,
        },
        {
            "title": f"{keyword} Wall Art Poster",
            "platform": "Society6",
            "price": 27.00,
            "reviews": 485,
        },
    ]

    return products