# NicheScanner AI

NicheScanner AI is a beginner-friendly Python command-line application for researching print-on-demand niche ideas. It stores product examples, imports user CSV research files, scans marketplace keyword results, scores demand signals, estimates competition, detects simple Niche DNA categories, finds promising opportunities, exports research data to CSV, and generates a static HTML dashboard.

Current version: v1.6.2

Release v1.6.2 makes eBay OAuth client credentials the preferred token source when `EBAY_CLIENT_ID` and `EBAY_CLIENT_SECRET` are present, while keeping `EBAY_APPLICATION_TOKEN` as a fallback. Release v1.6.1 added end-to-end eBay debug output for keyword scans, database inserts, and dashboard exports.

## What It Does

NicheScanner AI provides a small research workflow for product niche exploration:

1. Import sample products with title, platform, price, reviews, and rating.
2. Import your own product research from a CSV file.
3. Scan a keyword using Etsy and eBay when configured, with a safe mock fallback.
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
- Keyword Scanner: optional Etsy and eBay keyword search with safe mock fallback in `core/connectors/`.
- Etsy Product Details: stores listing ID, product URL, image URL, shop name, shop URL, currency, price, Shop Rating, and Shop Reviews when available.
- Niche DNA Engine: rule-based product type, topic, subtopic, and detected keyword classification using `core/engine/` modules and `core/knowledge/knowledge_base.json`.
- Competition Engine: simple competition labels calculated in `core/scoring.py` from review counts: Very High, High, Medium, or Low.
- Opportunity Finder: identifies products with strong demand, healthy pricing, and good niche scores in `core/opportunity_finder.py`.
- Opportunity Score 2.0: scoring includes demand, competition, price, trend, data confidence, overall score, and opportunity labels.
- CSV Export: exports product details, rating, scores, competition, opportunity, and Niche DNA fields to `reports/nichescanner_report.csv`.
- HTML Dashboard: generates `reports/dashboard.html` with summary cards and a sortable product table.
- SQLite storage: stores products locally in `data/nichescanner.db`, with safe migration support for `rating` and optional Etsy detail columns.
- Keyword trends: counts repeated words in stored product titles.
- Mock fallback: keeps keyword scanning usable when Etsy and eBay are not configured or both external requests fail.

## Opportunity Score 2.0

Opportunity Score 2.0 is a transparent multi-factor scoring model in `core/scoring.py`. It keeps the final score on a 0-100 scale, but breaks the result into components so users can understand why a product looks promising.

Components:

- Demand Score: estimates market demand from product review volume and rating when product-level data is available.
- Competition Score: estimates competitive pressure from review volume. Lower pressure produces a higher competition score.
- Price Score: measures whether the product price is in a healthy print-on-demand research range.
- Trend Score: reserved for Google Trends signal input. When no live trend signal is available, it safely uses `0`.
- Data Confidence: estimates trust in the available marketplace data. Etsy is High, eBay is Medium because product reviews are unavailable from the eBay Browse API, and mock/fallback data is Low.
- Overall Score: combines the components with weighted averages: Demand 35%, Price 25%, Competition 20%, Trend 10%, and Data Confidence 10%.

Score labels:

- `★★★★★ Excellent`
- `★★★★ Good`
- `★★★ Average`
- `★★ Weak`
- `★ Poor`
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
12. Show connector status
13. Exit
```

## Connector Manager

NicheScanner AI uses a Connector Manager in `core/connectors/connector_manager.py` to coordinate optional product and trend integrations from one place.

Current connector behavior:

- Etsy: used for product search only when `ETSY_KEYSTRING` and `ETSY_SHARED_SECRET` are configured and the API request succeeds.
- Google Trends: used only when optional `pytrends` is installed and the request succeeds.
- eBay: used for product search when `EBAY_APPLICATION_TOKEN` is configured, or when `EBAY_CLIENT_ID` and `EBAY_CLIENT_SECRET` can retrieve an OAuth token and the Browse API request succeeds.
- Pinterest: planned future connector.

For product search, the Connector Manager queries Etsy first, then eBay, and returns the combined product list when either connector returns products. Mock product data is used only when both Etsy and eBay return no products. All external integrations are optional. If an API key, optional package, or external request is unavailable, the app falls back safely to mock product data or fallback trend values.

## Optional Etsy API Integration

NicheScanner AI can optionally use Etsy Open API v3 for keyword scans. The app does not require Etsy credentials; when Etsy credentials are missing or an Etsy request fails, the Connector Manager can still use eBay when configured. Mock product data is used only when both marketplace connectors return no products.

To configure Etsy, set `ETSY_KEYSTRING` and `ETSY_SHARED_SECRET` as environment variables or in a local `.env` file:

```text
ETSY_KEYSTRING=your_etsy_keystring_here
ETSY_SHARED_SECRET=your_etsy_shared_secret_here
```

Do not commit `.env` or any API keys. When Etsy search succeeds, NicheScanner AI imports product title, platform, price, currency, listing ID, product URL, product image, shop name, shop URL, Shop Rating, and Shop Reviews when those fields are available from Etsy. Etsy enrichment uses the batch listing endpoint so product images and shop data are fetched with a single batch request instead of one request per product. This keeps typical Etsy scans near 7-8 seconds instead of approximately 2 minutes. Etsy public API batch responses do not provide listing-level aggregate ratings, so Shop Rating and Shop Reviews represent the shop rather than the individual product listing.

## Optional eBay API Integration

NicheScanner AI v1.6 can optionally use the official eBay Browse API for keyword scans. The Connector Manager queries Etsy first and eBay second, then aggregates results from both marketplaces. If one connector fails or returns no products, products from the other connector are still used. If both connectors return no products, the app falls back safely to mock product data.

To prepare eBay credentials, copy `.env.example` to `.env` in the project root and fill in either `EBAY_APPLICATION_TOKEN` for temporary application-token testing, or `EBAY_CLIENT_ID` and `EBAY_CLIENT_SECRET` for the OAuth client credentials flow:

```powershell
Copy-Item .env.example .env
```

Your local `.env` file should use this format:

```text
EBAY_CLIENT_ID=your_ebay_client_id_here
EBAY_CLIENT_SECRET=your_ebay_client_secret_here
EBAY_APPLICATION_TOKEN=your_ebay_application_token_here
```

The app does not require eBay credentials to run. When these values are missing, the eBay connector reports `eBay API not configured.` and fails safely. When `EBAY_APPLICATION_TOKEN` is present, the connector uses it directly as a bearer token and skips the OAuth request. When it is missing, the connector keeps the existing OAuth flow using `EBAY_CLIENT_ID` and `EBAY_CLIENT_SECRET`. When eBay search succeeds, NicheScanner AI imports product title, platform, price, currency, item ID, item URL, product image, seller name, condition, category, and shipping price when those fields are available from eBay. eBay seller feedback is seller-level reputation, so it is not used as product review or rating data.

Use menu option `12. Show connector status` to check whether eBay is configured. The check reports whether credentials are present, whether a usable token can be found or retrieved, and whether a small product search can run. Do not commit `.env` or any real API credentials.

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
- Shop Rating
- Shop Reviews
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
13
```

Expected result:

- Products are cleared and sample products are imported.
- The report shows rating, rating score, competition, and opportunity.
- The HTML dashboard is created at `reports/dashboard.html`.
- Top Niches shows rating and competition.
- Hidden Opportunities runs without crashing.
- CSV export creates `reports/nichescanner_report.csv`.

For marketplace-enabled scans, the dashboard also shows clickable product links and product thumbnails when Etsy or eBay returns image URLs.

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
    market_scanner.py          Keyword scanner entry point
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
- v1.5: Rich Etsy product data import, faster batch-based Etsy scans, shop-level rating/review display, and dashboard display
- v1.6: eBay marketplace integration, application-token support, and aggregated Etsy + eBay keyword scan results
- v1.6.1: End-to-end eBay debug output for connector calls, Browse API item counts, SQLite inserts, and dashboard product counts
- v1.6.2: eBay OAuth client credentials now take priority over the older application token fallback

Future direction:

- v1.7: Multi marketplace intelligence
- v1.8: Advanced scoring engine
- v2.0: AI niche intelligence

## Limitations

- Keyword scanning queries Etsy first, then eBay, and aggregates both result sets when available.
- Mock fallback is used only when both Etsy and eBay return no products.
- CSV import expects the required columns listed above.
- Imported CSV rows use `CSV Import` as the platform.
- The HTML dashboard is a static generated file.
- No live marketplace scraping is implemented; optional Etsy and eBay support use official APIs.
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
- Enriched Etsy imports with listing ID, product URL, image URL, shop name, shop URL, currency, price, Shop Rating, and Shop Reviews when available.
- Optimized Etsy scans with the Etsy batch endpoint, reducing typical scan time from approximately 2 minutes to around 7-8 seconds.
- Fetched product images and shop data with a single batch request instead of one request per product.
- Displayed product thumbnails, clickable product links, Shop Rating, and Shop Reviews in the Streamlit dashboard.
- Clarified that Etsy Shop Rating and Shop Reviews are shop-level metrics because Etsy public batch listing responses do not provide listing-level aggregate ratings.
- Kept mock fallback and older SQLite databases compatible.

### v1.6

- Added optional official eBay Browse API keyword search.
- Added temporary support for `EBAY_APPLICATION_TOKEN` from `.env` for application-token testing.
- Kept the existing eBay OAuth client credentials flow with `EBAY_CLIENT_ID` and `EBAY_CLIENT_SECRET` when no application token is present.
- Normalized eBay products with title, platform, price, currency, item URL, image URL, seller, condition, category, shipping price, seller feedback score, and seller feedback percentage.
- Updated the Connector Manager to query Etsy and eBay, aggregate both result sets, and use mock fallback only when both connectors return no products.
- Kept scoring, dashboard behavior, and database schema compatible with existing product rows.
