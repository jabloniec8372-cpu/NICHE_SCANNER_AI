from database import create_database
from database import add_product
from database import get_products
from database import clear_products
from market_scanner import scan_keyword
from report_exporter import export_products_to_csv
from keyword_analyzer import analyze_keywords
from engine.niche_dna_engine import build_niche_dna
from scoring import calculate_score


def show_menu():
    print("===================================")
    print("     NICHE SCANNER AI v0.9.1")
    print("===================================")
    print()
    print("1. Import sample products")
    print("2. Show report")
    print("3. Scan keyword")
    print("4. Clear products")
    print("5. Export CSV report")
    print("6. Show keyword trends")
    print("7. Show Niche DNA")
    print("8. Exit")
    print()

    return input("Choose option: ")


def import_products():
    add_product("Funny Cat Shirt", "Etsy", 19.99, 842)
    add_product("Camping Dad Shirt", "Etsy", 22.50, 620)
    add_product("Nurse Coffee Shirt", "Redbubble", 24.00, 1200)
    add_product("Funny German Shepherd Hoodie", "Etsy", 29.99, 930)
    add_product("Camping Grandpa Coffee Mug", "Etsy", 16.50, 410)

    print()
    print("[OK] Sample products imported.")
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

    for product in products:
        was_inserted = add_product(
            product["title"],
            product["platform"],
            product["price"],
            product["reviews"]
        )

        if was_inserted:
            imported_count += 1

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
        title, platform, price, reviews = product
        score = calculate_score(price, reviews)

        print(f"Title: {title}")
        print(f"Platform: {platform}")
        print(f"Price: ${price}")
        print(f"Reviews: {reviews}")
        print(f"Trend Score: {score}/100")
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
        title, platform, price, reviews = product
        dna = build_niche_dna(title)

        print(f"Title: {dna['title']}")
        print(f"Product Type: {dna['product_type']}")
        print(f"Main Topic: {dna['main_topic']}")
        print(f"Subtopic: {dna['subtopic']}")
        print(f"Detected Keyword: {dna['detected_keyword']}")
        print("--------------------------------")

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


def clear_products_menu():
    clear_products()

    print()
    print("[OK] Products cleared.")
    print()


def main():
    create_database()

    while True:
        choice = show_menu()

        if choice == "1":
            import_products()

        elif choice == "2":
            show_report()

        elif choice == "3":
            scan_keyword_menu()

        elif choice == "4":
            clear_products_menu()

        elif choice == "5":
            export_report_menu()

        elif choice == "6":
            show_keyword_trends()

        elif choice == "7":
            show_niche_dna()

        elif choice == "8":
            print()
            print("[OK] Goodbye!")
            break

        else:
            print()
            print("[ERROR] Invalid option.")
            print()


if __name__ == "__main__":
    main()
