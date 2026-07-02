import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ETSY_PING_URL = "https://openapi.etsy.com/v3/application/openapi-ping"
ETSY_SEARCH_URL = "https://openapi.etsy.com/v3/application/listings/active"
DEBUG_RESPONSE_LIMIT = 300


def get_etsy_keystring():
    keystring = os.environ.get("ETSY_KEYSTRING", "").strip()

    if keystring:
        return keystring

    return _read_value_from_env_file("ETSY_KEYSTRING")


def get_etsy_shared_secret():
    shared_secret = os.environ.get("ETSY_SHARED_SECRET", "").strip()

    if shared_secret:
        return shared_secret

    return _read_value_from_env_file("ETSY_SHARED_SECRET")


def get_etsy_api_key():
    keystring = get_etsy_keystring()
    shared_secret = get_etsy_shared_secret()

    if not keystring or not shared_secret:
        return ""

    return f"{keystring}:{shared_secret}"


def is_etsy_configured():
    return bool(get_etsy_api_key())


def search_etsy_products(keyword, limit=10):
    api_key = get_etsy_api_key()

    if not api_key:
        return []

    requests = _get_requests_module()

    if requests is None:
        print("[INFO] Etsy API credentials found, but the requests package is not installed.")
        print("[INFO] Using mock product data instead.")
        return []

    if not _is_etsy_key_accepted(requests, api_key):
        print("[INFO] Etsy API credentials were not accepted by Etsy ping endpoint.")
        print("[INFO] Using mock product data instead.")
        return []

    try:
        response = requests.get(
            ETSY_SEARCH_URL,
            headers=_build_etsy_headers(api_key),
            params={
                "keywords": keyword,
                "limit": limit
            },
            timeout=10
        )

        if not response.ok:
            _print_etsy_response_debug("listing search", response)
            return []
    except requests.RequestException as error:
        print("[INFO] Etsy listing search failed. Using mock product data instead.")
        print(error)
        return []

    try:
        data = response.json()
    except ValueError:
        print("[INFO] Etsy API returned an invalid JSON response. Using mock product data instead.")
        _print_response_text_preview(response)
        return []

    listings = data.get("results", [])
    products = []

    for listing in listings:
        product = _normalize_listing(listing)

        if product:
            products.append(product)

    return products


def _get_requests_module():
    try:
        import requests
        return requests
    except ImportError:
        return None


def _is_etsy_key_accepted(requests, api_key):
    try:
        response = requests.get(
            ETSY_PING_URL,
            headers=_build_etsy_headers(api_key),
            timeout=10
        )
    except requests.RequestException as error:
        print("[INFO] Etsy ping request failed. Using mock product data instead.")
        print(error)
        return False

    if not response.ok:
        _print_etsy_response_debug("openapi ping", response)
        return False

    return True


def _build_etsy_headers(api_key):
    return {
        "x-api-key": api_key,
        "Accept": "application/json"
    }


def _print_etsy_response_debug(action, response):
    print(f"[INFO] Etsy {action} failed. Using mock product data instead.")
    print(f"[INFO] Etsy status code: {response.status_code}")
    _print_response_text_preview(response)


def _print_response_text_preview(response):
    response_text = str(getattr(response, "text", ""))
    preview = response_text[:DEBUG_RESPONSE_LIMIT]

    if preview:
        print(f"[INFO] Etsy response preview: {preview}")
    else:
        print("[INFO] Etsy response preview: <empty response>")


def _read_value_from_env_file(variable_name):
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

                if name.strip() == variable_name:
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