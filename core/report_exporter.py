import csv
from pathlib import Path

from engine.niche_dna_engine import build_niche_dna
from product_utils import product_to_dict
from scoring import calculate_score


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = PROJECT_ROOT / "reports" / "nichescanner_report.csv"


def format_marketplace_metric(platform, value):
    if str(platform).lower() == "ebay" and value == 0:
        return "N/A"

    return value


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
            "Overall Score",
            "Score Badge",
            "Demand Score",
            "Competition Score",
            "Trend Score",
            "Price Score",
            "Data Confidence",
            "Confidence Score",
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

            score = calculate_score(price, reviews, rating, platform)
            dna = build_niche_dna(title)

            writer.writerow([
                title,
                platform,
                price,
                product_data["currency"],
                format_marketplace_metric(platform, rating),
                format_marketplace_metric(platform, reviews),
                product_data["listing_id"],
                product_data["product_url"],
                product_data["image_url"],
                product_data["shop_name"],
                product_data["shop_url"],
                score["overall_score"],
                score["score_badge"],
                score["demand_score"],
                score["competition_score"],
                score["trend_score"],
                score["price_score"],
                score["confidence"],
                score["confidence_score"],
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