from html import escape
from pathlib import Path

from engine.niche_dna_engine import build_niche_dna
from opportunity_finder import find_hidden_opportunities
from product_utils import product_to_dict
from scoring import calculate_score


EBAY_REVIEW_NOTE = "Product review data is unavailable from the eBay Browse API."


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_PATH = PROJECT_ROOT / "reports" / "dashboard.html"


def export_dashboard(products):
    DASHBOARD_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Build the dashboard data first, then turn it into one static HTML file.
    dashboard_rows = _build_dashboard_rows(products)
    ebay_products_count = sum(
        1 for row in dashboard_rows
        if str(row["platform"]).lower() == "ebay"
    )
    print(f"[DASHBOARD] ebay products count: {ebay_products_count}")
    summary = _build_summary(products, dashboard_rows)
    html = _build_html(summary, dashboard_rows)

    with open(DASHBOARD_PATH, "w", encoding="utf-8") as file:
        file.write(html)

    return DASHBOARD_PATH


def _build_dashboard_rows(products):
    rows = []

    for product in products:
        product_data = product_to_dict(product)
        title = product_data["title"]
        platform = product_data["platform"]
        price = product_data["price"]
        reviews = product_data["reviews"]
        rating = product_data["rating"]

        # Reuse the same scoring and Niche DNA logic used by the CLI reports.
        score = calculate_score(price, reviews, rating, platform)
        dna = build_niche_dna(title)

        rows.append({
            "title": title,
            "platform": platform,
            "price": price,
            "rating": format_marketplace_metric(platform, rating),
            "reviews": format_marketplace_metric(platform, reviews),
            "score": score["overall_score"],
            "score_badge": score["score_badge"],
            "demand_score": score["demand_score"],
            "competition_score": score["competition_score"],
            "trend_score": score["trend_score"],
            "price_score": score["price_score"],
            "confidence": score["confidence"],
            "competition": score["competition"],
            "opportunity": score["opportunity"],
            "product_type": dna["product_type"],
            "main_topic": dna["main_topic"],
            "subtopic": dna["subtopic"],
            "listing_id": product_data["listing_id"],
            "product_url": product_data["product_url"],
            "image_url": product_data["image_url"],
            "shop_name": product_data["shop_name"],
            "shop_url": product_data["shop_url"],
            "currency": product_data["currency"]
        })

    return rows

def format_marketplace_metric(platform, value):
    if str(platform).lower() == "ebay" and value == 0:
        return "N/A"

    return value


def _build_summary(products, rows):
    total_products = len(rows)

    # Empty databases still get a valid dashboard with zeroed summary cards.
    if total_products:
        average_score = round(
            sum(row["score"] for row in rows) / total_products,
            1
        )
        best_row = max(rows, key=lambda row: row["score"])
        best_product = best_row["title"]
    else:
        average_score = 0
        best_product = "No products yet"

    hidden_opportunities = find_hidden_opportunities(products)

    return {
        "total_products": total_products,
        "average_score": average_score,
        "best_product": best_product,
        "hidden_opportunities": len(hidden_opportunities)
    }


def _build_html(summary, rows):
    table_rows = "\n".join(_build_table_row(row) for row in rows)
    note_html = ""

    if _has_unavailable_ebay_product_data(rows):
        note_html = f'<div class="data-note">{escape(EBAY_REVIEW_NOTE)}</div>'

    # CSS and JavaScript stay inline so the dashboard works as one standalone file.
    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>NicheScanner AI Dashboard</title>
    <style>
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            color: #1f2933;
            background: #f4f7fb;
        }}

        header {{
            padding: 24px 32px;
            background: #14213d;
            color: #ffffff;
        }}

        h1 {{
            margin: 0 0 8px;
            font-size: 28px;
        }}

        main {{
            padding: 24px 32px;
        }}

        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}

        .card {{
            padding: 16px;
            border: 1px solid #d9e2ec;
            border-radius: 8px;
            background: #ffffff;
        }}

        .label {{
            margin-bottom: 8px;
            color: #627d98;
            font-size: 13px;
            text-transform: uppercase;
        }}

        .value {{
            font-size: 24px;
            font-weight: bold;
        }}

        .table-wrap {{
            overflow-x: auto;
            border: 1px solid #d9e2ec;
            border-radius: 8px;
            background: #ffffff;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            min-width: 1100px;
        }}

        th,
        td {{
            padding: 12px;
            border-bottom: 1px solid #e5eaf0;
            text-align: left;
            white-space: nowrap;
        }}

        th {{
            cursor: pointer;
            background: #eef2f7;
            user-select: none;
        }}

        tr:hover td {{
            background: #f8fafc;
        }}

        img.thumbnail {{
            width: 64px;
            height: 64px;
            object-fit: cover;
            border-radius: 6px;
            border: 1px solid #d9e2ec;
            background: #f8fafc;
            cursor: zoom-in;
        }}

        a {{
            color: #1d4ed8;
            font-weight: bold;
        }}
        .image-preview {{
            position: fixed;
            inset: 0;
            z-index: 1000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 32px;
            background: rgba(15, 23, 42, 0.72);
        }}

        .image-preview.is-open {{
            display: flex;
        }}

        .image-preview-panel {{
            position: relative;
            max-width: min(880px, 92vw);
            max-height: 88vh;
        }}

        .image-preview-panel img {{
            display: block;
            max-width: 100%;
            max-height: 88vh;
            border-radius: 8px;
            background: #ffffff;
            box-shadow: 0 24px 64px rgba(15, 23, 42, 0.35);
        }}

        .image-preview-close {{
            position: absolute;
            top: 8px;
            right: 8px;
            width: 36px;
            height: 36px;
            border: 0;
            border-radius: 50%;
            background: rgba(15, 23, 42, 0.88);
            color: #ffffff;
            cursor: pointer;
            font-size: 24px;
            line-height: 36px;
        }}
    </style>
</head>
<body>
    <header>
        <h1>NicheScanner AI Dashboard</h1>
        <div>Static HTML report generated from stored product data.</div>
    </header>

    <main>
        <section class="summary">
            <div class="card">
                <div class="label">Total Products</div>
                <div class="value">{summary["total_products"]}</div>
            </div>
            <div class="card">
                <div class="label">Average Score</div>
                <div class="value">{summary["average_score"]}</div>
            </div>
            <div class="card">
                <div class="label">Best Product</div>
                <div class="value">{escape(str(summary["best_product"]))}</div>
            </div>
            <div class="card">
                <div class="label">Hidden Opportunities</div>
                <div class="value">{summary["hidden_opportunities"]}</div>
            </div>
        </section>

        {note_html}
        <section class="table-wrap">
            <table id="product-table">
                <thead>
                    <tr>
                        <th>Image</th>
                        <th onclick="sortTable(1)">Title</th>
                        <th onclick="sortTable(2)">Platform</th>
                        <th onclick="sortTable(3)">Price</th>
                        <th onclick="sortTable(4)">Shop Rating</th>
                        <th onclick="sortTable(5)">Shop Reviews</th>
                        <th onclick="sortTable(6)">Score</th>
                        <th onclick="sortTable(7)">Score Badge</th>
                        <th onclick="sortTable(8)">Demand</th>
                        <th onclick="sortTable(9)">Competition Score</th>
                        <th onclick="sortTable(10)">Trend</th>
                        <th onclick="sortTable(11)">Price Score</th>
                        <th onclick="sortTable(12)">Confidence</th>
                        <th onclick="sortTable(13)">Competition</th>
                        <th onclick="sortTable(14)">Opportunity</th>
                        <th onclick="sortTable(15)">Product</th>
                        <th onclick="sortTable(16)">Shop</th>
                        <th onclick="sortTable(17)">Listing ID</th>
                        <th onclick="sortTable(18)">Product Type</th>
                        <th onclick="sortTable(19)">Main Topic</th>
                        <th onclick="sortTable(20)">Subtopic</th>
                    </tr>
                </thead>
                <tbody>
{table_rows}
                </tbody>
            </table>
        </section>
    </main>
    <div class="image-preview" id="image-preview" aria-hidden="true">
        <div class="image-preview-panel" role="dialog" aria-modal="true" aria-label="Product image preview">
            <button class="image-preview-close" id="image-preview-close" type="button" aria-label="Close image preview">X</button>
            <img id="image-preview-img" src="" alt="">
        </div>
    </div>

    <script>
        var sortDirections = {{}};
        var imagePreview = document.getElementById("image-preview");
        var imagePreviewImg = document.getElementById("image-preview-img");
        var imagePreviewClose = document.getElementById("image-preview-close");
        function sortTable(columnIndex) {{
            closeImagePreview();
            var table = document.getElementById("product-table");
            var tbody = table.tBodies[0];
            var rows = Array.from(tbody.rows);
            var direction = sortDirections[columnIndex] === "asc" ? "desc" : "asc";

            sortDirections[columnIndex] = direction;

            rows.sort(function (a, b) {{
                var aValue = a.cells[columnIndex].textContent.trim();
                var bValue = b.cells[columnIndex].textContent.trim();
                var aNumber = parseFloat(aValue.replace("$", ""));
                var bNumber = parseFloat(bValue.replace("$", ""));

                if (!isNaN(aNumber) && !isNaN(bNumber)) {{
                    return direction === "asc" ? aNumber - bNumber : bNumber - aNumber;
                }}

                return direction === "asc"
                    ? aValue.localeCompare(bValue)
                    : bValue.localeCompare(aValue);
            }});

            rows.forEach(function (row) {{
                tbody.appendChild(row);
            }});
        }}
        function openImagePreview(imageElement) {{
            imagePreviewImg.src = imageElement.src;
            imagePreviewImg.alt = imageElement.alt || "Product image preview";
            imagePreview.classList.add("is-open");
            imagePreview.setAttribute("aria-hidden", "false");
        }}

        function closeImagePreview() {{
            if (!imagePreview.classList.contains("is-open")) {{
                return;
            }}

            imagePreview.classList.remove("is-open");
            imagePreview.setAttribute("aria-hidden", "true");
            imagePreviewImg.src = "";
            imagePreviewImg.alt = "";
        }}

        document.addEventListener("click", function (event) {{
            var thumbnail = event.target.closest("img.thumbnail");

            if (thumbnail) {{
                event.stopPropagation();
                openImagePreview(thumbnail);
                return;
            }}

            if (event.target === imagePreview || event.target === imagePreviewClose) {{
                closeImagePreview();
                return;
            }}

            if (!event.target.closest(".image-preview-panel")) {{
                closeImagePreview();
            }}
        }});

        document.addEventListener("keydown", function (event) {{
            if (event.key === "Escape") {{
                closeImagePreview();
            }}
        }});

        window.addEventListener("scroll", closeImagePreview, {{ passive: true }});
    </script>
</body>
</html>
"""


def _has_unavailable_ebay_product_data(rows):
    return any(
        str(row["platform"]).lower() == "ebay"
        and (row["reviews"] == "N/A" or row["rating"] == "N/A")
        for row in rows
    )


def _build_table_row(row):
    # Escape every displayed value so product titles cannot break the HTML.
    image_html = ""
    if row["image_url"]:
        image_html = (
            f'<img class="thumbnail" src="{escape(str(row["image_url"]), quote=True)}" '
            f'alt="{escape(str(row["title"]), quote=True)}">'
        )

    product_link_html = ""
    if row["product_url"]:
        product_link_html = (
            f'<a href="{escape(str(row["product_url"]), quote=True)}" target="_blank" '
            f'rel="noopener noreferrer">Open</a>'
        )

    shop_text = escape(str(row["shop_name"]))
    if row["shop_url"]:
        shop_text = (
            f'<a href="{escape(str(row["shop_url"]), quote=True)}" target="_blank" '
            f'rel="noopener noreferrer">{shop_text or "Shop"}</a>'
        )

    price_text = f'{row["currency"]} {row["price"]}'.strip()

    return f"""                    <tr>
                        <td>{image_html}</td>
                        <td>{escape(str(row["title"]))}</td>
                        <td>{escape(str(row["platform"]))}</td>
                        <td>{escape(str(price_text))}</td>
                        <td>{escape(str(row["rating"]))}</td>
                        <td>{escape(str(row["reviews"]))}</td>
                        <td>{escape(str(row["score"]))}</td>
                        <td>{escape(str(row["score_badge"]))}</td>
                        <td>{escape(str(row["demand_score"]))}</td>
                        <td>{escape(str(row["competition_score"]))}</td>
                        <td>{escape(str(row["trend_score"]))}</td>
                        <td>{escape(str(row["price_score"]))}</td>
                        <td>{escape(str(row["confidence"]))}</td>
                        <td>{escape(str(row["competition"]))}</td>
                        <td>{escape(str(row["opportunity"]))}</td>
                        <td>{product_link_html}</td>
                        <td>{shop_text}</td>
                        <td>{escape(str(row["listing_id"]))}</td>
                        <td>{escape(str(row["product_type"]))}</td>
                        <td>{escape(str(row["main_topic"]))}</td>
                        <td>{escape(str(row["subtopic"]))}</td>
                    </tr>"""
