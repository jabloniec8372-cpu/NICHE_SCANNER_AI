from connectors.ebay_connector import is_ebay_configured
from connectors.etsy_api import is_etsy_configured, search_etsy_products
from connectors.google_trends import (
    get_google_trend_summary,
    is_google_trends_available,
)


def search_all_sources(keyword, product_limit=50):
    etsy_products = search_etsy_products(keyword, limit=product_limit)

    if etsy_products:
        print(f"[DEBUG] Connector source used: Etsy")
        print(f"[DEBUG] Products returned: {len(etsy_products)}")
        return etsy_products

    mock_products = _get_mock_products(keyword)
    print(f"[DEBUG] Connector source used: Mock")
    print(f"[DEBUG] Products returned: {len(mock_products)}")
    return mock_products


def get_connector_status():
    etsy_configured = is_etsy_configured()
    ebay_configured = is_ebay_configured()
    google_trends_configured = is_google_trends_available()

    return {
        "etsy": {
            "configured": etsy_configured,
            "status": "Configured" if etsy_configured else "Using mock fallback"
        },
        "google_trends": {
            "configured": google_trends_configured,
            "status": "Available" if google_trends_configured else "Optional dependency missing"
        },
        "ebay": {
            "configured": ebay_configured,
            "status": "Configured" if ebay_configured else "eBay API not configured."
        },
        "pinterest": {
            "configured": False,
            "status": "Planned"
        }
    }


def get_trend_summary(keyword):
    try:
        return get_google_trend_summary(keyword)
    except Exception as error:
        return {
            "keyword": str(keyword).strip(),
            "source": "Google Trends",
            "available": False,
            "trend_score": 0,
            "trend_direction": "Unavailable",
            "message": f"Trend connector failed safely: {error}"
        }


def _get_mock_products(keyword):
    print("[INFO] Using mock product data fallback.")
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

    for product in products:
        product.setdefault("rating", 0)
        product.setdefault("listing_id", "")
        product.setdefault("product_url", "")
        product.setdefault("image_url", "")
        product.setdefault("shop_name", "")
        product.setdefault("shop_url", "")
        product.setdefault("currency", "USD")

    return products
