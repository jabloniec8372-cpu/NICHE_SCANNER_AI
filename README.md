# NicheScanner AI

NicheScanner AI is a beginner-friendly Python command-line application for exploring print-on-demand niche ideas. It helps collect product examples, score simple market signals, analyze repeated keywords, classify products into a basic Niche DNA profile, and export research results to CSV.

Current version: v0.9.1

This project is prepared for GitHub as part of the v0.9 release line. It currently uses offline mock market data only; it does not scrape live marketplaces or call external APIs.

## What It Does

NicheScanner AI provides a small research workflow for product niche exploration:

1. Add sample product data.
2. Scan a keyword using mock product results.
3. Store products in a local SQLite database.
4. Generate a terminal report with trend scores.
5. Analyze common keywords in product titles.
6. Detect product type and topic using Niche DNA analysis.
7. Export results to a CSV report.

## Current Features

- Sample product import
- Report generation
- Keyword scanning with offline mock data
- Product clearing
- CSV export
- Keyword trends
- Niche DNA analysis
- SQLite storage in `data/nichescanner.db`
- Shared trend scoring logic
- Beginner-friendly terminal menu

## Installation On Windows

1. Install Python 3.11 or newer from the official Python website.
2. During installation, enable **Add python.exe to PATH**.
3. Open PowerShell.
4. Clone or download this repository.
5. Go to the project folder:

```powershell
cd C:\NICHE_SCANNER_AI
```

No external Python packages are required for the current version. The project uses only the Python standard library.

## Run The App

From the project root:

```powershell
cd C:\NICHE_SCANNER_AI
python core\main.py
```

The app opens an interactive menu:

```text
1. Import sample products
2. Show report
3. Scan keyword
4. Clear products
5. Export CSV report
6. Show keyword trends
7. Show Niche DNA
8. Exit
```

## CSV Export

CSV reports are written to:

```text
reports/nichescanner_report.csv
```

The export includes product details, trend score, product type, main topic, subtopic, and detected keyword.

## Project Structure

```text
NICHE_SCANNER_AI/
  README.md                 Project overview and usage guide
  ROADMAP.md                Planned release direction
  AGENTS.md                 Repository development rules

  core/
    main.py                 CLI menu and application flow
    database.py             SQLite database helpers
    scoring.py              Shared trend score calculation
    market_scanner.py       Offline mock keyword scanner
    keyword_analyzer.py     Product title keyword analysis
    report_exporter.py      CSV report export
    sample_data.py          Reserved for sample data helpers

    config/
      categories.py         Product type keyword configuration
      topics.py             Topic configuration reference

    engine/
      category_engine.py    Product type detection
      topic_engine.py       Topic detection from knowledge base
      niche_dna_engine.py   Combined Niche DNA output

    knowledge/
      knowledge_base.json   Topic and keyword knowledge base

  data/
    nichescanner.db         Local SQLite database

  reports/
    nichescanner_report.csv Exported CSV report
```

## Portfolio Value

NicheScanner AI demonstrates practical Python automation and product research logic in a small, readable codebase. It shows:

- Python command-line application structure
- SQLite data storage
- CSV processing
- Keyword analysis
- Rule-based product classification
- Reusable scoring logic
- Beginner-friendly documentation and project organization

This makes the project suitable as a portfolio example for Python automation, data processing, and early-stage market research tooling.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full roadmap.

Planned direction:

- v0.9: GitHub polish and documentation
- v1.0: Real marketplace data research
- v1.1: Improved scoring system
- v1.2: Dashboard and export improvements
- v2.0: Optional AI-assisted niche recommendations

## Limitations

- Keyword scanning uses mock data only.
- No live marketplace scraping is implemented.
- No external AI recommendations are implemented.
- The scoring system is intentionally simple.
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
