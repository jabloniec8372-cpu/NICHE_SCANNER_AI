from html import escape
from pathlib import Path

from engine.niche_dna_engine import build_niche_dna
from opportunity_finder import find_hidden_opportunities
from scoring import calculate_score


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_PATH = PROJECT_ROOT / "reports" / "dashboard.html"


def export_dashboard(products):
    DASHBOARD_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Build the dashboard data first, then turn it into one static HTML file.
    dashboard_rows = _build_dashboard_rows(products)
    summary = _build_summary(products, dashboard_rows)
    html = _build_html(summary, dashboard_rows)

    with open(DASHBOARD_PATH, "w", encoding="utf-8") as file:
        file.write(html)

    return DASHBOARD_PATH


def _build_dashboard_rows(products):
    rows = []

    for product in products:
        title, platform, price, reviews, rating = product

        # Reuse the same scoring and Niche DNA logic used by the CLI reports.
        score = calculate_score(price, reviews, rating)
        dna = build_niche_dna(title)

        rows.append({
            "title": title,
            "platform": platform,
            "price": price,
            "rating": rating,
            "reviews": reviews,
            "score": score["total_score"],
            "competition": score["competition"],
            "opportunity": score["opportunity"],
            "product_type": dna["product_type"],
            "main_topic": dna["main_topic"],
            "subtopic": dna["subtopic"]
        })

    return rows


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

        <section class="table-wrap">
            <table id="product-table">
                <thead>
                    <tr>
                        <th onclick="sortTable(0)">Title</th>
                        <th onclick="sortTable(1)">Platform</th>
                        <th onclick="sortTable(2)">Price</th>
                        <th onclick="sortTable(3)">Rating</th>
                        <th onclick="sortTable(4)">Reviews</th>
                        <th onclick="sortTable(5)">Score</th>
                        <th onclick="sortTable(6)">Competition</th>
                        <th onclick="sortTable(7)">Opportunity</th>
                        <th onclick="sortTable(8)">Product Type</th>
                        <th onclick="sortTable(9)">Main Topic</th>
                        <th onclick="sortTable(10)">Subtopic</th>
                    </tr>
                </thead>
                <tbody>
{table_rows}
                </tbody>
            </table>
        </section>
    </main>

    <script>
        var sortDirections = {{}};

        function sortTable(columnIndex) {{
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
    </script>
</body>
</html>
"""


def _build_table_row(row):
    # Escape every displayed value so product titles cannot break the HTML.
    return f"""                    <tr>
                        <td>{escape(str(row["title"]))}</td>
                        <td>{escape(str(row["platform"]))}</td>
                        <td>${escape(str(row["price"]))}</td>
                        <td>{escape(str(row["rating"]))}</td>
                        <td>{escape(str(row["reviews"]))}</td>
                        <td>{escape(str(row["score"]))}</td>
                        <td>{escape(str(row["competition"]))}</td>
                        <td>{escape(str(row["opportunity"]))}</td>
                        <td>{escape(str(row["product_type"]))}</td>
                        <td>{escape(str(row["main_topic"]))}</td>
                        <td>{escape(str(row["subtopic"]))}</td>
                    </tr>"""