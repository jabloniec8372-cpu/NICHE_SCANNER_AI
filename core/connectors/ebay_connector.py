import base64
import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
EBAY_TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"
EBAY_BROWSE_SEARCH_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"
EBAY_SCOPE = "https://api.ebay.com/oauth/api_scope"
DEBUG_RESPONSE_LIMIT = 300
DEFAULT_LIMIT = 50


def get_ebay_client_id():
    client_id = os.environ.get("EBAY_CLIENT_ID", "").strip()

    if client_id:
        return client_id

    return _read_value_from_env_file("EBAY_CLIENT_ID")


def get_ebay_client_secret():
    client_secret = os.environ.get("EBAY_CLIENT_SECRET", "").strip()

    if client_secret:
        return client_secret

    return _read_value_from_env_file("EBAY_CLIENT_SECRET")


def is_ebay_configured():
    return bool(get_ebay_client_id() and get_ebay_client_secret())


def get_ebay_access_token():
    client_id = get_ebay_client_id()
    client_secret = get_ebay_client_secret()

    if not client_id or not client_secret:
        print("eBay API not configured.")
        return ""

    requests = _get_requests_module()

    if requests is None:
        print("[INFO] eBay API credentials found, but the requests package is not installed.")
        return ""

    credentials = f"{client_id}:{client_secret}".encode("utf-8")
    encoded_credentials = base64.b64encode(credentials).decode("ascii")

    try:
        response = requests.post(
            EBAY_TOKEN_URL,
            headers={
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "client_credentials",
                "scope": EBAY_SCOPE,
            },
            timeout=10,
        )
        print(f"[INFO] eBay OAuth status code: {response.status_code}")

        if not response.ok:
            print("[INFO] eBay OAuth failed. Check EBAY_CLIENT_ID and EBAY_CLIENT_SECRET.")
            _print_response_text_preview(response)
            return ""

        data = response.json()
    except requests.RequestException as error:
        print("[INFO] eBay OAuth request failed safely.")
        print(error)
        return ""
    except ValueError:
        print("[INFO] eBay OAuth returned an invalid JSON response.")
        _print_response_text_preview(response)
        return ""

    access_token = str(data.get("access_token", "")).strip()

    if not access_token:
        print("[INFO] eBay OAuth response did not include an access token.")

    return access_token


def search_ebay_products(keyword, limit=DEFAULT_LIMIT):
    print(f"[INFO] eBay search starts for keyword: {keyword}")

    clean_keyword = str(keyword).strip()

    if not clean_keyword:
        print("[INFO] eBay search skipped because keyword is empty.")
        return []

    access_token = get_ebay_access_token()

    if not access_token:
        return []

    requests = _get_requests_module()

    if requests is None:
        print("[INFO] eBay API credentials found, but the requests package is not installed.")
        return []

    wanted_products = _safe_positive_int(limit, DEFAULT_LIMIT)

    try:
        response = requests.get(
            EBAY_BROWSE_SEARCH_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
            params={
                "q": clean_keyword,
                "limit": wanted_products,
            },
            timeout=10,
        )
        print(f"[INFO] eBay Browse search status code: {response.status_code}")

        if not response.ok:
            print("[INFO] eBay Browse API search failed safely.")
            _print_response_text_preview(response)
            return []

        data = response.json()
    except requests.RequestException as error:
        print("[INFO] eBay Browse search failed safely.")
        print(error)
        return []
    except ValueError:
        print("[INFO] eBay Browse search returned invalid JSON.")
        _print_response_text_preview(response)
        return []

    item_summaries = data.get("itemSummaries", [])

    if not isinstance(item_summaries, list):
        print("[INFO] eBay Browse search returned no item summaries.")
        return []

    products = []

    for item in item_summaries:
        product = _normalize_item(item)

        if product:
            products.append(product)

    return products


def _normalize_item(item):
    if not isinstance(item, dict):
        return None

    title = str(item.get("title", "")).strip()

    if not title:
        return None

    item_id = _clean_value(item.get("itemId"))
    item_url = _clean_value(item.get("itemWebUrl"))
    image_url = _extract_image_url(item)
    seller_name = _extract_seller_name(item)
    condition = _clean_value(item.get("condition"))
    shipping_price = _extract_shipping_price(item)

    return {
        "title": title,
        "platform": "eBay",
        "price": _extract_price(item),
        "currency": _extract_currency(item),
        "item_id": item_id,
        "item_url": item_url,
        "image_url": image_url,
        "seller_name": seller_name,
        "condition": condition,
        "shipping_price": shipping_price,
        "reviews": _extract_seller_feedback_score(item),
        "rating": _extract_seller_feedback_percentage(item),
        "listing_id": item_id,
        "product_url": item_url,
        "shop_name": seller_name,
        "shop_url": "",
    }


def _extract_price(item):
    return _extract_money_value(item.get("price", {}))


def _extract_currency(item):
    price_data = item.get("price", {})

    if not isinstance(price_data, dict):
        return ""

    return _clean_value(price_data.get("currency"))


def _extract_shipping_price(item):
    shipping_options = item.get("shippingOptions", [])

    if not isinstance(shipping_options, list) or not shipping_options:
        return 0.0

    first_option = shipping_options[0]

    if not isinstance(first_option, dict):
        return 0.0

    return _extract_money_value(first_option.get("shippingCost", {}))


def _extract_money_value(money_data):
    if not isinstance(money_data, dict):
        return 0.0

    return _safe_float(money_data.get("value"), 0)


def _extract_image_url(item):
    image_data = item.get("image", {})

    if isinstance(image_data, dict):
        return _clean_value(image_data.get("imageUrl"))

    return ""


def _extract_seller_name(item):
    seller_data = item.get("seller", {})

    if not isinstance(seller_data, dict):
        return ""

    return _clean_value(seller_data.get("username"))


def _extract_seller_feedback_score(item):
    seller_data = item.get("seller", {})

    if not isinstance(seller_data, dict):
        return 0

    return _safe_positive_int(seller_data.get("feedbackScore"), 0)


def _extract_seller_feedback_percentage(item):
    seller_data = item.get("seller", {})

    if not isinstance(seller_data, dict):
        return 0

    return _safe_float(seller_data.get("feedbackPercentage"), 0)


def _get_requests_module():
    try:
        import requests
        return requests
    except ImportError:
        return None


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


def _print_response_text_preview(response):
    response_text = str(getattr(response, "text", ""))
    preview = response_text[:DEBUG_RESPONSE_LIMIT]

    if preview:
        print(f"[INFO] eBay response preview: {preview}")
    else:
        print("[INFO] eBay response preview: <empty response>")


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
