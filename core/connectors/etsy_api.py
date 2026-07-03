import os
from pathlib import Path

from pod_filter import is_pod_product


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ETSY_PING_URL = "https://openapi.etsy.com/v3/application/openapi-ping"
ETSY_SEARCH_URL = "https://openapi.etsy.com/v3/application/listings/active"
ETSY_BATCH_LISTINGS_URL = "https://openapi.etsy.com/v3/application/listings/batch"
ETSY_LISTING_IMAGES_URL = "https://openapi.etsy.com/v3/application/listings/{listing_id}/images"
ETSY_SHOP_URL = "https://openapi.etsy.com/v3/application/shops/{shop_id}"

DEBUG_RESPONSE_LIMIT = 300
DEFAULT_LIMIT = 50
MAX_ETSY_PAGE_LIMIT = 100
MAX_RAW_LISTINGS_TO_SCAN = 150


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
    return bool(get_etsy_keystring() and get_etsy_shared_secret())


def search_etsy_products(keyword, limit=DEFAULT_LIMIT):
    api_key = get_etsy_api_key()
    print(f"[INFO] Etsy search starts for keyword: {keyword}")
    print(f"[INFO] Etsy keystring present: {bool(api_key)}")

    if not api_key:
        return []

    requests = _get_requests_module()

    if requests is None:
        print("[INFO] Etsy API credentials found, but the requests package is not installed.")
        return []

    if not _is_etsy_key_accepted(requests, api_key):
        print("[INFO] Etsy API credentials were not accepted by Etsy ping endpoint.")
        return []

    wanted_products = _safe_positive_int(limit, DEFAULT_LIMIT)
    raw_scan_limit = max(wanted_products * 3, wanted_products)
    raw_scan_limit = min(raw_scan_limit, MAX_RAW_LISTINGS_TO_SCAN)

    listings = _fetch_etsy_listings(
        requests=requests,
        api_key=api_key,
        keyword=keyword,
        raw_scan_limit=raw_scan_limit,
    )

    print(f"[INFO] Etsy raw listings collected: {len(listings)}")

    pod_listings = [
        listing
        for listing in listings
        if is_pod_product(str(listing.get("title", "")))
    ][:wanted_products]
    enriched_listings = _fetch_batch_listing_details(
        requests=requests,
        api_key=api_key,
        listings=pod_listings,
    )
    products = []

    for listing in enriched_listings:
        product = _normalize_listing(listing)

        if product:
            product["opportunity_score"] = _calculate_opportunity_score(product)
            products.append(product)

    products.sort(key=lambda item: item.get("opportunity_score", 0), reverse=True)

    print(f"[INFO] Etsy POD products after filter: {len(products)}")
    return products[:wanted_products]


def _fetch_etsy_listings(requests, api_key, keyword, raw_scan_limit):
    listings = []
    offset = 0

    while len(listings) < raw_scan_limit:
        page_limit = min(MAX_ETSY_PAGE_LIMIT, raw_scan_limit - len(listings))

        try:
            response = requests.get(
                ETSY_SEARCH_URL,
                headers=_build_etsy_headers(api_key),
                params={
                    "keywords": keyword,
                    "limit": page_limit,
                    "offset": offset,
                },
                timeout=10,
            )
            print(
                f"[INFO] Etsy listing search status code: {response.status_code} "
                f"(limit={page_limit}, offset={offset})"
            )

            if not response.ok:
                _print_etsy_response_debug("listing search", response)
                break

            data = response.json()
        except requests.RequestException as error:
            print("[INFO] Etsy listing search failed.")
            print(error)
            break
        except ValueError:
            print("[INFO] Etsy API returned an invalid JSON response.")
            _print_response_text_preview(response)
            break

        page_results = data.get("results", [])

        if not isinstance(page_results, list) or not page_results:
            break

        listings.extend(page_results)

        if len(page_results) < page_limit:
            break

        offset += page_limit

    return listings


def _fetch_batch_listing_details(requests, api_key, listings):
    listing_ids = [
        _clean_value(listing.get("listing_id"))
        for listing in listings
        if _clean_value(listing.get("listing_id"))
    ]

    if not listing_ids:
        return listings

    try:
        response = requests.get(
            ETSY_BATCH_LISTINGS_URL,
            headers=_build_etsy_headers(api_key),
            params={
                "listing_ids": ",".join(listing_ids),
                "includes": "Images,Shop",
            },
            timeout=15,
        )
        print(f"[INFO] Etsy batch listing status code: {response.status_code}")

        if not response.ok:
            _print_etsy_response_debug("batch listing lookup", response)
            return listings

        data = response.json()
    except requests.RequestException as error:
        print("[INFO] Etsy batch listing lookup failed.")
        print(error)
        return listings
    except ValueError:
        print("[INFO] Etsy batch listing lookup returned invalid JSON.")
        _print_response_text_preview(response)
        return listings

    results = data.get("results", [])

    if not isinstance(results, list):
        return listings

    listings_by_id = {
        _clean_value(listing.get("listing_id")): listing
        for listing in results
    }

    return [
        listings_by_id.get(_clean_value(listing.get("listing_id")), listing)
        for listing in listings
    ]


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
            timeout=10,
        )
        print(f"[INFO] Etsy ping status code: {response.status_code}")
    except requests.RequestException as error:
        print("[INFO] Etsy ping request failed.")
        print(error)
        return False

    if not response.ok:
        print("[INFO] Etsy openapi ping failed.")
        print(f"[INFO] Etsy status code: {response.status_code}")
        _print_response_text_preview(response)
        return False

    return True


def _build_etsy_headers(api_key):
    return {
        "x-api-key": api_key,
        "Accept": "application/json",
    }


def _print_etsy_response_debug(action, response):
    print(f"[INFO] Etsy {action} failed.")
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


def _normalize_listing(listing, requests=None, api_key="", shop_cache=None):
    title = str(listing.get("title", "")).strip()

    if not title:
        return None

    price = _extract_price(listing)
    currency = _extract_currency(listing)
    listing_id = _clean_value(listing.get("listing_id"))
    shop_id = _clean_value(listing.get("shop_id"))
    product_url = str(listing.get("url", "")).strip()
    image_url = _extract_image_url(listing)
    shop = _extract_shop(listing)
    shop_name = _clean_value(shop.get("shop_name") or shop.get("title"))
    shop_url = _clean_value(shop.get("url"))
    reviews = _safe_positive_int(shop.get("review_count"), 0)
    rating = _safe_float(shop.get("review_average"), 0)
    favorites = _safe_positive_int(
        listing.get("num_favorers") or listing.get("favorers") or listing.get("favorites"),
        0,
    )
    views = _safe_positive_int(listing.get("views"), 0)

    if requests and api_key:
        if listing_id and not image_url:
            image_url = _fetch_listing_image_url(requests, api_key, listing_id)

        if shop_id and (not shop_name or not shop_url):
            shop_details = _fetch_shop_details(requests, api_key, shop_id, shop_cache)
            shop_name = shop_name or _clean_value(
                shop_details.get("shop_name") or shop_details.get("title")
            )
            shop_url = shop_url or _clean_value(shop_details.get("url"))

    return {
        "title": title,
        "platform": "Etsy",
        "price": price,
        "reviews": reviews,
        "rating": rating,
        "listing_id": listing_id,
        "product_url": product_url,
        "image_url": image_url,
        "shop_name": shop_name,
        "shop_url": shop_url,
        "currency": currency,
        "favorites": favorites,
        "views": views,
    }


def _calculate_opportunity_score(product):
    score = 0

    title = product.get("title", "").lower()
    price = float(product.get("price") or 0)
    favorites = _safe_positive_int(product.get("favorites"), 0)
    views = _safe_positive_int(product.get("views"), 0)

    score += min(favorites * 2, 40)
    score += min(views / 25, 20)

    if 12 <= price <= 35:
        score += 15
    elif 8 <= price <= 50:
        score += 8

    strong_pod_words = [
        "shirt",
        "t-shirt",
        "tee",
        "hoodie",
        "sweatshirt",
        "mug",
        "sticker",
        "poster",
        "wall art",
        "print",
        "tote",
    ]

    emotional_words = [
        "funny",
        "gift",
        "mom",
        "dad",
        "nurse",
        "teacher",
        "dog",
        "cat",
        "wedding",
        "retro",
        "vintage",
        "christmas",
        "birthday",
    ]

    if any(word in title for word in strong_pod_words):
        score += 15

    if any(word in title for word in emotional_words):
        score += 10

    if product.get("image_url"):
        score += 10

    return round(score, 2)


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


def _extract_currency(listing):
    price_data = listing.get("price", {})

    if isinstance(price_data, dict):
        return _clean_value(price_data.get("currency_code"))

    return _clean_value(listing.get("currency_code"))


def _extract_image_url(listing):
    images = listing.get("Images") or listing.get("images") or []

    if not images:
        return ""

    first_image = images[0]

    if not isinstance(first_image, dict):
        return ""

    for field_name in ("url_fullxfull", "url_570xN", "url_300x300", "url_170x135"):
        image_url = first_image.get(field_name)

        if image_url:
            return str(image_url)

    return ""


def _extract_shop(listing):
    shop = listing.get("Shop") or listing.get("shop") or {}

    if isinstance(shop, dict):
        return shop

    return {}


def _fetch_listing_image_url(requests, api_key, listing_id):
    try:
        response = requests.get(
            ETSY_LISTING_IMAGES_URL.format(listing_id=listing_id),
            headers=_build_etsy_headers(api_key),
            timeout=10,
        )

        if not response.ok:
            print(f"[INFO] Etsy image lookup failed for listing {listing_id}: {response.status_code}")
            return ""

        data = response.json()
    except (requests.RequestException, ValueError) as error:
        print(f"[INFO] Etsy image lookup failed safely for listing {listing_id}.")
        print(error)
        return ""

    images = data.get("results", [])

    if not isinstance(images, list) or not images:
        return ""

    return _extract_image_url({"Images": images})


def _fetch_shop_details(requests, api_key, shop_id, shop_cache):
    if shop_cache is None:
        shop_cache = {}

    if shop_id in shop_cache:
        return shop_cache[shop_id]

    try:
        response = requests.get(
            ETSY_SHOP_URL.format(shop_id=shop_id),
            headers=_build_etsy_headers(api_key),
            timeout=10,
        )

        if not response.ok:
            print(f"[INFO] Etsy shop lookup failed for shop {shop_id}: {response.status_code}")
            shop_cache[shop_id] = {}
            return {}

        data = response.json()
    except (requests.RequestException, ValueError) as error:
        print(f"[INFO] Etsy shop lookup failed safely for shop {shop_id}.")
        print(error)
        data = {}

    if not isinstance(data, dict):
        data = {}

    shop_cache[shop_id] = data
    return data


def _safe_positive_int(value, default=0):
    try:
        number = int(float(value))
    except (TypeError, ValueError):
        return default

    if number < 0:
        return default

    return number


def _safe_float(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clean_value(value):
    if value is None:
        return ""

    return str(value).strip()