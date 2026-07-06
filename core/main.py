from database import create_database
from database import add_product
from database import get_products
from database import clear_products
from csv_importer import import_products_from_csv
from dashboard_exporter import export_dashboard
from market_scanner import scan_keyword
from report_exporter import export_products_to_csv
from keyword_analyzer import analyze_keywords
from engine.niche_dna_engine import build_niche_dna
from product_utils import product_to_dict
from scoring import calculate_score
from opportunity_finder import find_hidden_opportunities
from connectors.connector_manager import get_connector_status
from connectors.ebay_connector import check_ebay_connection


def show_menu():
    print("===================================")
    print("     NICHE SCANNER AI v1.6.2")
    print("===================================")
    print()
    print("1. Import sample products")
    print("2. Import products from CSV")
    print("3. Show report")
    print("4. Scan keyword")
    print("5. Clear products")
    print("6. Export CSV report")
    print("7. Generate HTML dashboard")
    print("8. Show keyword trends")
    print("9. Show Niche DNA")
    print("10. Show Top Niches")
    print("11. Hidden Opportunities")
    print("12. Show connector status")
    print("13. Exit")
    print()

    return input("Choose option: ")


def import_products():
    add_product("Funny Cat Shirt", "Etsy", 19.99, 842, 4.7)
    add_product("Camping Dad Shirt", "Etsy", 22.50, 620, 4.6)
    add_product("Nurse Coffee Shirt", "Redbubble", 24.00, 1200, 4.9)
    add_product("Funny German Shepherd Hoodie", "Etsy", 29.99, 930, 4.8)
    add_product("Camping Grandpa Coffee Mug", "Etsy", 16.50, 410, 4.4)

    print()
    print("[OK] Sample products imported.")
    print()


def import_products_from_csv_menu():
    file_path = input("Enter CSV file path: ").strip()

    if not file_path:
        print()
        print("[ERROR] CSV file path cannot be empty.")
        print()
        return

    products = import_products_from_csv(file_path)
    imported_count = 0

    for product in products:
        was_inserted = add_product(
            product["title"],
            product["platform"],
            product["price"],
            product["reviews"],
            product["rating"]
        )

        if was_inserted:
            imported_count += 1

    print(f"[OK] Imported {imported_count} new products from CSV.")
    print()

def scan_keyword_menu():
    keyword = input("Enter keyword: ").strip()

    if not keyword:
        print()
        print("[ERROR] Keyword cannot be empty.")
        print()
        return

    print()
    print(f"[SCAN] Scanning keyword: {keyword}")
    print()

    products = scan_keyword(keyword)
    imported_count = 0
    inserted_ebay_count = 0

    for product in products:
        was_inserted = add_product(
            product["title"],
            product["platform"],
            product["price"],
            product["reviews"],
            product.get("rating", 0),
            product.get("listing_id", ""),
            product.get("product_url", ""),
            product.get("image_url", ""),
            product.get("shop_name", ""),
            product.get("shop_url", ""),
            product.get("currency", "")
        )

        if was_inserted:
            imported_count += 1
            if str(product.get("platform", "")).lower() == "ebay":
                inserted_ebay_count += 1

    print(f"[DB] inserted ebay products count: {inserted_ebay_count}")
    print(f"[OK] Imported {imported_count} new products.")
    print()

def show_report():
    products = get_products()

    print()
    print("========== NICHE SCANNER REPORT ==========")
    print()

    if not products:
        print("No products in database yet.")
        print()
        return

    for product in products:
        product_data = product_to_dict(product)
        title = product_data["title"]
        platform = product_data["platform"]
        price = product_data["price"]
        reviews = product_data["reviews"]
        rating = product_data["rating"]
        score = calculate_score(price, reviews, rating, platform)

        print(f"Title: {title}")
        print(f"Platform: {platform}")
        print(f"Price: {_format_price(price, product_data['currency'])}")
        print(f"Reviews: {reviews}")
        print(f"Rating: {rating}")
        if product_data["listing_id"]:
            print(f"Listing ID: {product_data['listing_id']}")
        if product_data["product_url"]:
            print(f"Product URL: {product_data['product_url']}")
        if product_data["shop_name"]:
            print(f"Shop: {product_data['shop_name']}")
        if product_data["shop_url"]:
            print(f"Shop URL: {product_data['shop_url']}")
        print(f"Overall Score: {score['overall_score']}/100")
        print(f"Score Badge: {score['score_badge']}")
        print(f"Demand Score: {score['demand_score']}/100")
        print(f"Competition Score: {score['competition_score']}/100")
        print(f"Trend Score: {score['trend_score']}/100")
        print(f"Price Score: {score['price_score']}/100")
        print(f"Data Confidence: {score['confidence']}")
        print(f"Competition: {score['competition']}")
        print(f"Opportunity: {score['opportunity']}")
        print("------------------------------------------")

    print()


def show_keyword_trends():
    products = get_products()

    if not products:
        print()
        print("[ERROR] No products to analyze.")
        print()
        return

    keywords = analyze_keywords(products)

    print()
    print("========== KEYWORD TRENDS ==========")
    print()

    for word, count in keywords:
        print(f"{word}: {count}")

    print()


def show_niche_dna():
    products = get_products()

    if not products:
        print()
        print("[ERROR] No products to analyze.")
        print()
        return

    print()
    print("========== NICHE DNA ==========")
    print()

    for product in products:
        product_data = product_to_dict(product)
        title = product_data["title"]
        dna = build_niche_dna(title)

        print(f"Title: {dna['title']}")
        print(f"Product Type: {dna['product_type']}")
        print(f"Main Topic: {dna['main_topic']}")
        print(f"Subtopic: {dna['subtopic']}")
        print(f"Detected Keyword: {dna['detected_keyword']}")
        print("--------------------------------")

    print()


def show_top_niches():
    products = get_products()

    if not products:
        print()
        print("[ERROR] No products to analyze.")
        print()
        return

    ranked_products = []

    for product in products:
        product_data = product_to_dict(product)
        title = product_data["title"]
        platform = product_data["platform"]
        price = product_data["price"]
        reviews = product_data["reviews"]
        rating = product_data["rating"]
        score = calculate_score(price, reviews, rating, platform)

        ranked_products.append({
            "title": title,
            "platform": platform,
            "price": price,
            "reviews": reviews,
            "rating": rating,
            "currency": product_data["currency"],
            "score": score
        })

    ranked_products.sort(
        key=lambda item: item["score"]["total_score"],
        reverse=True
    )

    print()
    print("========== TOP NICHES ==========")
    print()

    for index, item in enumerate(ranked_products[:10], start=1):
        print(f"{index}. {item['title']}")
        print(f"   Platform: {item['platform']}")
        print(f"   Price: {_format_price(item['price'], item['currency'])}")
        print(f"   Reviews: {item['reviews']}")
        print(f"   Rating: {item['rating']}")
        print(f"   Competition: {item['score']['competition']}")
        print(f"   Overall Score: {item['score']['overall_score']}/100")
        print(f"   Demand: {item['score']['demand_score']}/100")
        print(f"   Competition Score: {item['score']['competition_score']}/100")
        print(f"   Price: {item['score']['price_score']}/100")
        print(f"   Confidence: {item['score']['confidence']}")
        print(f"   Opportunity: {item['score']['opportunity']}")
        print("--------------------------------")
        print()

    print()


def _format_price(price, currency=""):
    if currency:
        return f"{currency} {price:.2f}"

    return f"${price:.2f}"


def show_hidden_opportunities():
    products = get_products()

    if not products:
        print()
        print("[ERROR] No products to analyze.")
        print()
        return

    opportunities = find_hidden_opportunities(products)

    print()
    print("========== HIDDEN OPPORTUNITIES ==========")
    print()

    if not opportunities:
        print("No hidden opportunities found.")
        print()
        return

    for item in opportunities:
        print(f"[OPPORTUNITY] {item['title']}")
        print(f"Platform: {item['platform']}")
        print(f"Price: ${item['price']}")
        print(f"Reviews: {item['reviews']}")
        print(f"Rating: {item['rating']}")
        print(f"Competition: {item['score']['competition']}")
        print(f"Overall Score: {item['score']['overall_score']}/100")
        print(f"Demand: {item['score']['demand_score']}/100")
        print(f"Competition Score: {item['score']['competition_score']}/100")
        print(f"Trend: {item['score']['trend_score']}/100")
        print(f"Price: {item['score']['price_score']}/100")
        print(f"Confidence: {item['score']['confidence']}")
        print("Reasons:")

        for reason in item["reasons"]:
            print(f"  - {reason}")

        print("------------------------------------------")
        print()

    print()


def export_report_menu():
    products = get_products()

    if not products:
        print()
        print("[ERROR] No products to export.")
        print()
        return

    export_products_to_csv(products)
    print()


def export_dashboard_menu():
    products = get_products()

    if not products:
        print()
        print("[ERROR] No products to export.")
        print()
        return

    dashboard_path = export_dashboard(products)

    print()
    print("[OK] HTML dashboard saved:")
    print(dashboard_path)
    print()


def clear_products_menu():
    clear_products()

    print()
    print("[OK] Products cleared.")
    print()

def _format_connector_label(connector_name):
    if connector_name == "ebay":
        return "eBay"

    return connector_name.replace("_", " ").title()

def show_connector_status_menu():
    connector_status = get_connector_status()

    print()
    print("========== CONNECTOR STATUS ==========")
    print()

    for connector_name, connector in connector_status.items():
        label = _format_connector_label(connector_name)
        print(f"{label}: {connector['status']}")

    print()
    print("========== EBAY CONNECTION CHECK ==========")
    ebay_check = check_ebay_connection()
    print(f"Credentials present: {'Yes' if ebay_check['configured'] else 'No'}")
    print(f"OAuth token retrieved: {'Yes' if ebay_check['oauth_token'] else 'No'}")
    print(f"Product search runnable: {'Yes' if ebay_check['search'] else 'No'}")
    print(f"Products found: {ebay_check['products_found']}")
    print(f"Message: {ebay_check['message']}")
    print()

def main():
    create_database()

    while True:
        choice = show_menu()

        if choice == "1":
            import_products()

        elif choice == "2":
            import_products_from_csv_menu()

        elif choice == "3":
            show_report()

        elif choice == "4":
            scan_keyword_menu()

        elif choice == "5":
            clear_products_menu()

        elif choice == "6":
            export_report_menu()

        elif choice == "7":
            export_dashboard_menu()

        elif choice == "8":
            show_keyword_trends()

        elif choice == "9":
            show_niche_dna()

        elif choice == "10":
            show_top_niches()

        elif choice == "11":
            show_hidden_opportunities()

        elif choice == "12":
            show_connector_status_menu()

        elif choice == "13":
            print()
            print("[OK] Goodbye!")
            break

        else:
            print()
            print("[ERROR] Invalid option.")
            print()


if __name__ == "__main__":
    main()
