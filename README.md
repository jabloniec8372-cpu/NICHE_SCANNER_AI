# NicheScanner AI

NicheScanner AI is a beginner-friendly Python command-line application for researching print-on-demand niche ideas. It stores product examples, imports user CSV research files, scans mock keyword results, scores demand signals, estimates competition, detects simple Niche DNA categories, finds promising opportunities, exports research data to CSV, and generates a static HTML dashboard.

Current version: v1.5

Release v1.5 improves the optional Etsy API integration. Keyword scans can now store and display richer Etsy product data, including product thumbnails, product links, listing IDs, shop names, shop links, currency, and price when Etsy returns those fields.

## What It Does

NicheScanner AI provides a small research workflow for product niche exploration:

1. Import sample products with title, platform, price, reviews, and rating.
2. Import your own product research from a CSV file.
3. Scan a keyword using Etsy when configured, with a safe mock fallback.
4. Store products in a local SQLite database.
5. Generate terminal reports with scores, rating details, competition, and opportunity labels.
6. Analyze common keywords in product titles.
7. Detect product type and topic using the Niche DNA engine.
8. Show ranked top niches.
9. Find hidden opportunities based on demand, price, and score.
10. Export product research to a CSV report.
11. Generate a static HTML dashboard.
12. Review richer product details in the Streamlit dashboard.

## Current Features

- CLI menu: beginner-friendly terminal menu with sample import, CSV import, report, scan, clear, export, dashboard, trends, Niche DNA, Top Niches, Hidden Opportunities, and exit options.
- CSV Product Import: imports user product research files with `title`, `price`, `reviews`, and `rating` columns.
- Keyword Scanner: optional Etsy keyword search with safe mock fallback in `core/connectors/`.
- Etsy Product Details: stores listing ID, product URL, image URL, shop name, shop URL, currency, and price when available.
- Niche DNA Engine: rule-based product type, topic, subtopic, and detected keyword classification using `core/engine/` modules and `core/knowledge/knowledge_base.json`.
- Competition Engine: simple competition labels calculated in `core/scoring.py` from review counts: Very High, High, Medium, or Low.
- Opportunity Finder: identifies products with strong demand, healthy pricing, and good niche scores in `core/opportunity_finder.py`.
- Rating and scoring logic: products support ratings, and scoring includes review score, price score, rating score, total score, competition, and opportunity.
- CSV Export: exports product details, rating, scores, competition, opportunity, and Niche DNA fields to `reports/nichescanner_report.csv`.
- HTML Dashboard: generates `reports/dashboard.html` with summary cards and a sortable product table.
- SQLite storage: stores products locally in `data/nichescanner.db`, with safe migration support for `rating` and optional Etsy detail columns.
- Keyword trends: counts repeated words in stored product titles.
- Mock fallback: keeps keyword scanning usable when Etsy is not configured or an external request fails.

## Installation On Windows

1. Install Python 3.11 or newer from the official Python website.
2. During installation, enable **Add python.exe to PATH**.
3. Open PowerShell.
4. Clone or download this repository.
5. Go to the project folder:

```powershell
cd C:\NICHE_SCANNER_AI
```

No external Python packages are required.

## Run The App

From the project root:

```powershell
python core\main.py
```

The app opens this interactive menu:

```text
1. Import sample products
2. Import products from CSV
3. Show report
4. Scan keyword
5. Clear products
6. Export CSV report
7. Generate HTML dashboard
8. Show keyword trends
9. Show Niche DNA
10. Show Top Niches
11. Hidden Opportunities
12. Exit
```

## Connector Manager

NicheScanner AI uses a Connector Manager in `core/connectors/connector_manager.py` to coordinate optional product and trend integrations from one place.

Current connector behavior:

- Etsy: used for product search only when `ETSY_KEYSTRING` and `ETSY_SHARED_SECRET` are configured and the API request succeeds.
- Google Trends: used only when optional `pytrends` is installed and the request succeeds.
- eBay: planned future connector.
- Pinterest: planned future connector.

All external integrations are optional. If an API key, optional package, or external request is unavailable, the app falls back safely to mock product data or fallback trend values.
## Optional Etsy API Integration

NicheScanner AI can optionally use Etsy Open API v3 for keyword scans. The app does not require Etsy credentials; when credentials are missing or a request fails, it falls back to mock product data.

To configure Etsy, set `ETSY_KEYSTRING` and `ETSY_SHARED_SECRET` as environment variables or in a local `.env` file:

```text
ETSY_KEYSTRING=your_etsy_keystring_here
ETSY_SHARED_SECRET=your_etsy_shared_secret_here
```

Do not commit `.env` or any API keys. When Etsy search succeeds, NicheScanner AI imports product title, platform, price, currency, listing ID, product URL, product image, shop name, and shop URL when those fields are available from Etsy. If image or shop enrichment fails for an individual listing, the product is still imported with the fields that were available.

## Optional Google Trends Integration

NicheScanner AI can optionally show Google Trends insight inside the Streamlit dashboard. This does not require Google API keys.

Google Trends support uses the optional `pytrends` package. It is not required for the app to run.

To enable it later:

```powershell
pip install pytrends
```

When `pytrends` is missing, unavailable, or Google Trends requests fail, NicheScanner AI uses safe fallback values and keeps the dashboard working.

## CSV Product Import

Use menu option `2. Import products from CSV` to import your own research file.

The CSV file must include these columns:

```text
title,price,reviews,rating
```

Example CSV:

```csv
title,price,reviews,rating
Funny Cat Tote Bag,18.99,420,4.7
Camping Dad Hoodie,34.50,815,4.6
Nurse Coffee Mug,16.99,230,4.8
Invalid Product,not-a-price,100,4.5
```

The importer will:

- Read the CSV path you enter in the terminal.
- Validate that required columns exist.
- Convert `price` to a decimal number.
- Convert `reviews` to a whole number.
- Convert `rating` to a decimal number.
- Skip invalid rows with clear messages.
- Store valid products in SQLite using `CSV Import` as the platform.

## HTML Dashboard

Use menu option `7. Generate HTML dashboard` to create:

```text
reports/dashboard.html
```

The dashboard includes summary cards for:

- Total products
- Average score
- Best product
- Hidden opportunities

It also includes a product table with:

- Image thumbnail
- Title
- Platform
- Price
- Currency
- Rating
- Reviews
- Listing ID
- Product URL
- Shop name
- Shop URL
- Score
- Competition
- Opportunity
- Product type
- Main topic
- Subtopic

Click a table header in the browser to sort the table by that column.

## Basic Test Flow

After starting the app, you can test the sample workflow with:

```text
5
1
3
7
10
11
6
12
```

Expected result:

- Products are cleared and sample products are imported.
- The report shows rating, rating score, competition, and opportunity.
- The HTML dashboard is created at `reports/dashboard.html`.
- Top Niches shows rating and competition.
- Hidden Opportunities runs without crashing.
- CSV export creates `reports/nichescanner_report.csv`.

For an Etsy-enabled scan, the Streamlit dashboard also shows clickable product links and product thumbnails when Etsy returns image URLs.

## CSV Export

CSV reports are written to:

```text
reports/nichescanner_report.csv
```

The export includes:

- Title
- Platform
- Price
- Currency
- Rating
- Reviews
- Listing ID
- Product URL
- Image URL
- Shop Name
- Shop URL
- Trend Score
- Review Score
- Price Score
- Rating Score
- Competition
- Opportunity
- Product Type
- Main Topic
- Subtopic
- Detected Keyword

## Project Structure

```text
NICHE_SCANNER_AI/
  README.md                    Project overview and usage guide
  ROADMAP.md                   Planned release direction
  AGENTS.md                    Repository development rules

  core/
    main.py                    CLI menu and application flow
    database.py                SQLite database helpers and rating migration
    csv_importer.py            CSV product import and validation
    dashboard_exporter.py      Static HTML dashboard export
    scoring.py                 Score, rating score, competition, and opportunity logic
    opportunity_finder.py      Hidden opportunity detection
    market_scanner.py          Offline mock keyword scanner
    keyword_analyzer.py        Product title keyword analysis
    report_exporter.py         CSV report export
    sample_data.py             Reserved for sample data helpers
    product_utils.py           Shared product row compatibility helpers

    config/
      categories.py            Product type keyword configuration
      topics.py                Topic configuration reference

    engine/
      category_engine.py       Product type detection
      topic_engine.py          Topic detection from knowledge base
      niche_dna_engine.py      Combined Niche DNA output

    knowledge/
      knowledge_base.json      Topic and keyword knowledge base

  data/
    nichescanner.db            Local SQLite database

  reports/
    nichescanner_report.csv    Exported CSV report
    dashboard.html             Static HTML dashboard
```

Note: competition logic is currently part of `core/scoring.py`; there is no separate competition engine file yet.

## Portfolio Value

NicheScanner AI demonstrates practical Python automation and product research logic in a small, readable codebase. It shows:

- Python command-line application structure
- SQLite data storage and safe schema migration
- CSV import and export
- CSV validation and data conversion
- Static HTML report generation
- Keyword analysis
- Rule-based product classification
- Reusable scoring logic
- Beginner-friendly documentation and project organization

This makes the project suitable as a portfolio example for Python automation, data processing, and early-stage market research tooling.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full roadmap.

Completed:

- v0.9: GitHub polish and documentation foundation
- v0.9.1: Path, validation, and scoring documentation fixes
- v1.2: Rating, competition, opportunity, Top Niches, and richer export support
- v1.2.1: GitHub polish and documentation update
- v1.3: CSV import for user product research files
- v1.4: Static HTML dashboard export
- v1.5: Rich Etsy product data import and dashboard display

Future direction:

- v1.6: Better trend and competition scoring
- v2.0: Optional AI-assisted niche recommendations

## Limitations

- Keyword scanning uses Etsy only when credentials are configured and Etsy requests succeed.
- CSV import expects the required columns listed above.
- Imported CSV rows use `CSV Import` as the platform.
- The HTML dashboard is a static generated file.
- No live marketplace scraping is implemented.
- No external AI recommendations are implemented.
- The scoring system is intentionally simple and transparent.
- The app is currently terminal-based only.

## Version Notes

### v0.9

- Added shared scoring in `core/scoring.py`.
- Replaced corrupted terminal symbols with ASCII labels.
- Added richer CSV export with Niche DNA columns.
- Improved mock keyword scanner output.
- Added beginner-friendly documentation.

### v0.9.1

- Fixed database, report, and knowledge-base paths so the app works from the project root and other working directories.
- Added validation for empty keyword scans.
- Scan imports now report the real number of newly inserted products.
- Added scoring model documentation in `core/scoring.py`.

### v1.2

- Added product rating support in the database and app workflow.
- Added safe SQLite migration for the `rating` column.
- Updated scoring to include review score, price score, rating score, total score, competition, and opportunity.
- Added Top Niches and Hidden Opportunities menu flows.
- Updated CSV export with rating, rating score, competition, and opportunity fields.

### v1.2.1

- Updated README documentation to match the current v1.2 codebase.
- Updated roadmap to mark completed versions and define future work from v1.3 onward.
- Expanded development rules in `AGENTS.md`.
- No application logic changes.

### v1.3

- Added CSV product import in `core/csv_importer.py`.
- Added CLI menu support for importing products from CSV.
- Added validation for required CSV columns.
- Added safe skipping for invalid CSV rows.
- Updated README and roadmap for the v1.3 release.

### v1.4

- Added static HTML dashboard generation in `core/dashboard_exporter.py`.
- Added CLI menu support for generating `reports/dashboard.html`.
- Added dashboard summary cards for total products, average score, best product, and hidden opportunities.
- Added sortable dashboard product table with score, competition, opportunity, and Niche DNA fields.
- Updated README and roadmap for the v1.4 release.

### v1.5

- Added safe SQLite columns for optional Etsy listing details.
- Enriched Etsy imports with listing ID, product URL, image URL, shop name, shop URL, currency, and price when available.
- Displayed product thumbnails and clickable product links in the Streamlit dashboard.
- Kept mock fallback and older SQLite databases compatible.
