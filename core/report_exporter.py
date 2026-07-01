import csv

from engine.niche_dna_engine import build_niche_dna
from scoring import calculate_score


def export_products_to_csv(products):
    file_path = "reports/nichescanner_report.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Title",
            "Platform",
            "Price",
            "Reviews",
            "Trend Score",
            "Product Type",
            "Main Topic",
            "Subtopic",
            "Detected Keyword"
        ])

        for product in products:
            title, platform, price, reviews = product
            score = calculate_score(price, reviews)
            dna = build_niche_dna(title)

            writer.writerow([
                title,
                platform,
                price,
                reviews,
                score,
                dna["product_type"],
                dna["main_topic"],
                dna["subtopic"],
                dna["detected_keyword"]
            ])

    print(f"[OK] CSV report saved: {file_path}")
