import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ETSY_SEARCH_URL = "https://openapi.etsy.com/v3/application/listings/active"


def get_etsy_keystring():
    keystring = os.environ.get("ETSY_KEYSTRING", "").strip()

    if keystring:
        return keystring

    return _read_keystring_from_env_file()


def is_etsy_configured():
    return bool(get_etsy_keystring())


def search_etsy_products(keyword, limit=10):
    keystring = get_etsy_keystring()

    if not keystring:
        return []

    try:
        import requests
    except ImportError:
        print("[INFO] Etsy API key found, but the requests package is not installed.")
        print("[INFO] Using mock product data instead.")
        return []

    try:
        response = requests.get(
            ETSY_SEARCH_URL,
            headers={"x-api-key": keystring},
            params={
                "keywords": keyword,
                "limit": limit,
                "includes": "Images"
            },
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as error:
        print("[INFO] Etsy API request failed. Using mock product data instead.")
        print(error)
        return []

    try:
        data = response.json()
    except ValueError:
        print("[INFO] Etsy API returned an invalid response. Using mock product data instead.")
        return []

    listings = data.get("results", [])
    products = []

    for listing in listings:
        product = _normalize_listing(listing)

        if product:
            products.append(product)

    return products


def _read_keystring_from_env_file():
    env_path = PROJECT_ROOT / ".env"

    if not env_path.exists():
        return ""

    try:
        with open(env_path, "r", encoding="utf-8") as file:
            for line in file:
                clean_line = line.strip()

                if not clean_line or clean_line.startswith("#"):
                    continue

                if "=" not in clean_line:
                    continue

                name, value = clean_line.split("=", 1)

                if name.strip() == "ETSY_KEYSTRING":
                    return value.strip().strip('"').strip("'")
    except OSError:
        return ""

    return ""


def _normalize_listing(listing):
    title = str(listing.get("title", "")).strip()

    if not title:
        return None

    price = _extract_price(listing)
    product_url = str(listing.get("url", "")).strip()
    image_url = _extract_image_url(listing)

    return {
        "title": title,
        "platform": "Etsy",
        "price": price,
        "reviews": 0,
        "rating": 0,
        "product_url": product_url,
        "image_url": image_url
    }


def _extract_price(listing):
    price_data = listing.get("price", {})

    if isinstance(price_data, dict):
        amount = price_data.get("amount")
        divisor = price_data.get("divisor") or 100

        try:
            return float(amount) / float(divisor)
        except (TypeError, ValueError, ZeroDivisionError):
            return 0.0

    try:
        return float(price_data)
    except (TypeError, ValueError):
        return 0.0


def _extract_image_url(listing):
    images = listing.get("Images") or listing.get("images") or []

    if not images:
        return ""

    first_image = images[0]

    if not isinstance(first_image, dict):
        return ""

    for field_name in ("url_fullxfull", "url_570xN", "url_170x135"):
        image_url = first_image.get(field_name)

        if image_url:
            return str(image_url)

    return ""