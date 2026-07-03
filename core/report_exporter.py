import csv
from pathlib import Path

from engine.niche_dna_engine import build_niche_dna
from product_utils import product_to_dict
from scoring import calculate_score


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = PROJECT_ROOT / "reports" / "nichescanner_report.csv"


def export_products_to_csv(products):
    with open(REPORT_PATH, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Title",
            "Platform",
            "Price",
            "Currency",
            "Rating",
            "Reviews",
            "Listing ID",
            "Product URL",
            "Image URL",
            "Shop Name",
            "Shop URL",
            "Trend Score",
            "Review Score",
            "Price Score",
            "Rating Score",
            "Competition",
            "Opportunity",
            "Product Type",
            "Main Topic",
            "Subtopic",
            "Detected Keyword"
        ])

        for product in products:

            product_data = product_to_dict(product)
            title = product_data["title"]
            platform = product_data["platform"]
            price = product_data["price"]
            reviews = product_data["reviews"]
            rating = product_data["rating"]

            score = calculate_score(price, reviews, rating)

            dna = build_niche_dna(title)

            writer.writerow([
                title,
                platform,
                price,
                product_data["currency"],
                rating,
                reviews,
                product_data["listing_id"],
                product_data["product_url"],
                product_data["image_url"],
                product_data["shop_name"],
                product_data["shop_url"],
                score["total_score"],
                score["review_score"],
                score["price_score"],
                score["rating_score"],
                score["competition"],
                score["opportunity"],
                dna["product_type"],
                dna["main_topic"],
                dna["subtopic"],
                dna["detected_keyword"]
            ])

    print()
    print(f"[OK] CSV report saved:")
    print(REPORT_PATH)
    print()
