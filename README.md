# NicheScanner AI

NicheScanner AI is a beginner-friendly Python command-line application for researching print-on-demand niche ideas. It stores product examples, scans mock keyword results, scores demand signals, estimates competition, detects simple Niche DNA categories, finds promising opportunities, and exports research data to CSV.

Current version: v1.2.1

Release v1.2.1 is a GitHub polish and documentation update for the current v1.2 codebase. The app remains offline, terminal-based, dependency-free, and built with the Python standard library.

## What It Does

NicheScanner AI provides a small research workflow for product niche exploration:

1. Import sample products with title, platform, price, reviews, and rating.
2. Scan a keyword using offline mock product results.
3. Store products in a local SQLite database.
4. Generate terminal reports with scores, rating details, competition, and opportunity labels.
5. Analyze common keywords in product titles.
6. Detect product type and topic using the Niche DNA engine.
7. Show ranked top niches.
8. Find hidden opportunities based on demand, price, and score.
9. Export product research to a CSV report.

## Current Features

- CLI menu: beginner-friendly terminal menu with import, report, scan, clear, export, trends, Niche DNA, Top Niches, Hidden Opportunities, and exit options.
- Keyword Scanner: offline mock keyword scanner in `core/market_scanner.py` for local testing without scraping or APIs.
- Niche DNA Engine: rule-based product type, topic, subtopic, and detected keyword classification using `core/engine/` modules and `core/knowledge/knowledge_base.json`.
- Competition Engine: simple competition labels calculated in `core/scoring.py` from review counts: Very High, High, Medium, or Low.
- Opportunity Finder: identifies products with strong demand, healthy pricing, and good niche scores in `core/opportunity_finder.py`.
- Rating and scoring logic: products support ratings, and scoring includes review score, price score, rating score, total score, competition, and opportunity.
- CSV Export: exports product details, rating, scores, competition, opportunity, and Niche DNA fields to `reports/nichescanner_report.csv`.
- SQLite storage: stores products locally in `data/nichescanner.db`, with safe migration support for the `rating` column.
- Keyword trends: counts repeated words in stored product titles.
- No external dependencies: uses only the Python standard library.

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
2. Show report
3. Scan keyword
4. Clear products
5. Export CSV report
6. Show keyword trends
7. Show Niche DNA
8. Show Top Niches
9. Hidden Opportunities
10. Exit
```

## Basic Test Flow

After starting the app, you can test the main workflow with:

```text
4
1
2
8
9
5
10
```

Expected result:

- Products are cleared and sample products are imported.
- The report shows rating, rating score, competition, and opportunity.
- Top Niches shows rating and competition.
- Hidden Opportunities runs without crashing.
- CSV export creates `reports/nichescanner_report.csv`.

## CSV Export

CSV reports are written to:

```text
reports/nichescanner_report.csv
```

The export includes:

- Title
- Platform
- Price
- Rating
- Reviews
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
    scoring.py                 Score, rating score, competition, and opportunity logic
    opportunity_finder.py      Hidden opportunity detection
    market_scanner.py          Offline mock keyword scanner
    keyword_analyzer.py        Product title keyword analysis
    report_exporter.py         CSV report export
    sample_data.py             Reserved for sample data helpers

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
```

Note: competition logic is currently part of `core/scoring.py`; there is no separate competition engine file yet.

## Portfolio Value

NicheScanner AI demonstrates practical Python automation and product research logic in a small, readable codebase. It shows:

- Python command-line application structure
- SQLite data storage and safe schema migration
- CSV processing
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

Future direction:

- v1.3: CSV import for user product research files
- v1.4: Dashboard or richer reporting
- v1.5: Better trend and competition scoring
- v2.0: Optional AI-assisted niche recommendations

## Limitations

- Keyword scanning uses mock data only.
- No live marketplace scraping is implemented.
- No external marketplace APIs are implemented.
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
